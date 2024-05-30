import numpy as np
import scipy as sp
import os
from os import environ
import sys
from lazylinop import LazyLinOp, mpad2
from lazylinop.basicops import block_diag, diag, eye
from lazylinop.wip.signal import fft, is_power_of_two, oa
import warnings
from warnings import warn

sys.setrecursionlimit(100000)
warnings.simplefilter(action='always')


def _dims(in1s: int, K: int, mode: str):
    """Return length of the output as a function
    of the length of the input, of the length of kernel
    and of the convolution mode.

    Args:
        in1s: ``int``
            Size of the input array (if 1d, number of rows if 2d).
        K: ``int``
            Length of the kernel.
        mode: ``str``
            Convolution mode.

    Returns:
        ``int``
    """
    imode = 0 * int(mode == 'full') + 1 * int(mode == 'valid') + \
        2 * int(mode == 'same') + 3 * int(mode == 'circ')
    return np.array([in1s + K - 1,  # full
                     in1s - K + 1,  # valid
                     in1s,  # same
                     in1s  # circ
                     ],
                    dtype=np.int_)[imode]


def _rmode(mode: str):
    """Return adjoint convolution mode.

    Args:
        mode: ``str``
            Convolution mode.

    Returns:
        ``str``
    """
    return {'full': 'valid', 'valid': 'full',
            'same': 'same', 'circ': 'circ'}[mode]


def _is_cplx(t1, t2):
    return 'complex' in str(t1) or 'complex' in str(t2)


def convolve(in1s: int, in2: np.ndarray, mode: str = 'full',
             method: str = 'scipy_convolve', workers: int = None):
    r"""Builds a :class:`.LazyLinOp` for the 1d convolution of
    signal(s) of size ``in1s`` with a kernel ``in2``.

    See below, ``in1s`` and ``in2`` for input sizes.
    See ``mode`` for output size.

    Args:
        in1s: ``int``
            Size of the first input signal(s).

            The input shape can be ``(in1s,)`` for a single signal and ``(in1s,
            b)`` for a batch of ``b`` signals (to compute one convolution per
            column of size ``in1s`` with 1d-array ``in2``).

            See ``workers`` for parallelization of the 2d-array case.

        in2: ``np.ndarray``
            Second input. Kernel to convolve with the signal.
            ``in2`` is always a 1d-array.
        mode: ``str``, optional
            - ``'full'``: compute full convolution including at points of
              non-complete overlapping of inputs. Output size is ``in1s +
              in2.size - 1``.
            - ``'valid'``: compute only fully overlapping part of the
              convolution. This is the 'full' center part of (output)
              size ``ins1 - in2.size + 1`` (``in2.size <= in1s``
              must be satisfied).
            - ``'same'``: compute only the center part of ``'full'`` to
              obtain an output size equal to the input size ``in1s``.
            - ``'circ'``: compute circular convolution (``in2.size <= in1s``
              must be satisfied).
        method: ``str``, optional
            - ``'scipy_convolve'``: (default) encapsulate
              ``scipy.signal.convolve``.

              It uses internally best SciPy method between ``'fft'`` and
              ``'direct'`` (see `scipy.signal.choose_conv_method <https://
              docs.scipy.org/doc/scipy/reference/generated/scipy.signal.
              choose_conv_method.html#scipy.signal.choose_conv_method>`_).

            - ``'auto'``: use best ``method`` available.

                - for ``mode='circ'`` use ``method='fft'``.
                - for any other mode use ``method='direct'`` if  ``in2.size <
                  log2(output_size)``, ``method='scipy_convolve'`` otherwise.
                Note that, according to their performance,
                ``method='toeplitz'`` and ``method='oa'`` are never considered.

            - ``'direct'``: direct computation using nested for-loops with
              Numba and parallelization (see ``workers``).
            - ``'toeplitz'``: encapsulate ``scipy.linalg.toeplitz`` if ``in1s <
              2048``, ``scipy.linalg.matmul_toeplitz`` otherwise.
            - ``'oa'``: use Lazylinop implementation of overlap-add method.
            - ``'fft'``: (only for ``mode='circ'``) compute circular
              convolution using SciPy FFT.
        workers: ``int``, optional
            The number of threads used to parallelize
            ``method='direct', 'toeplitz', 'scipy_convolve'`` using
            respectively Numba, NumPy and SciPy capabilities.
            Default is ``os.cpu_count()`` (number of CPU threads available).

            .. admonition:: Environment override

                ``workers`` can be overridden from the environment using
                ``NUMBA_NUM_THREADS`` for ``method='direct'`` and
                ``OMP_NUM_THREADS`` for ``method='toeplitz'``,
                ``'scipy_convolve'``.

    Returns:
        :class:`.LazyLinOp`

    Raises:
        TypeError
            in1s must be an int.
        ValueError
            size in1s < 0
        ValueError
            mode is not valid ('full' (default), 'valid', 'same' or 'circ').
        ValueError
            in2.size > in1s and mode='valid'
        ValueError
            in2.size > in1s and mode='circ'
        Exception
            in2 must be 1d array.
        ValueError
            method is not in:
            'auto',
            'direct',
            'toeplitz',
            'scipy_convolve',
            'oa',
            'fft',
        ValueError
            method='fft' works only with mode='circ'.

    Examples:
        >>> import numpy as np
        >>> from lazylinop.wip.signal import convolve
        >>> import scipy as sp
        >>> x = np.random.randn(1024)
        >>> kernel = np.random.randn(32)
        >>> c1 = convolve(x.shape[0], kernel, method='direct') @ x
        >>> c2 = sp.signal.convolve(x, kernel, method='auto')
        >>> np.allclose(c1, c2)
        True
        >>> N = 32768
        >>> x = np.random.randn(N)
        >>> kernel = np.random.randn(48)
        >>> c1 = convolve(N, kernel, mode='circ', method='fft') @ x
        >>> c2 = convolve(N, kernel, mode='circ', method='direct') @ x
        >>> np.allclose(c1, c2)
        True

    .. seealso::
        - `SciPy convolve function <https://docs.scipy.org/doc/scipy/
          reference/generated/scipy.signal.convolve.html>`_,
        - `SciPy oaconvolve function <https://docs.scipy.org/doc/scipy/
          reference/generated/scipy.signal.oaconvolve.html>`_,
        - `Overlap-add method <https://en.wikipedia.org/wiki/
          Overlap%E2%80%93add_method>`_,
        - `Circular convolution <https://en.wikipedia.org/wiki/
          Circular_convolution>`_,
        - `SciPy correlate function <https://docs.scipy.org/doc/scipy/
          reference/generated/scipy.signal.correlate.html>`_,
        - `SciPy matmul_toeplitz function <https://docs.scipy.org/doc/
          scipy/reference/generated/
          scipy.linalg.matmul_toeplitz.html#scipy.linalg.matmul_toeplitz>`_.
    """
    # never disable JIT except if env var NUMBA_DISABLE_JIT is used
    if 'NUMBA_DISABLE_JIT' in environ:
        disable_jit = int(environ['NUMBA_DISABLE_JIT'])
    else:
        disable_jit = 0

    if workers is None:
        workers = os.cpu_count()  # default

    if mode not in ['full', 'valid', 'same', 'circ']:
        raise ValueError("mode is not valid ('full' (default), 'valid', 'same'"
                         " or 'circ').")

    methods = [
        'auto',
        'direct',
        'toeplitz',
        'scipy_convolve',
        'oa',
        'fft'
    ]

    circmethods = [
        'auto',
        'direct',
        'fft'
    ]

    if mode == 'circ' and method not in circmethods:
        raise ValueError("mode 'circ' expects method" +
                         " to be in " + str(circmethods))

    if mode != 'circ' and method == 'fft':
        raise ValueError("method='fft' works only with mode='circ'.")

    if type(in1s) is not int:
        raise TypeError("in1s must be an int.")

    if in1s <= 0:
        raise ValueError("size in1s < 0")

    if len(in2.shape) >= 2:
        raise Exception("in2 must be 1d array.")

    K = in2.shape[0]
    if K > in1s and mode == 'valid':
        raise ValueError("in2.size > in1s and mode='valid'")
    if K > in1s and mode == 'circ':
        raise ValueError("in2.size > in1s and mode='circ'")

    if mode == 'circ':
        if method == 'auto':
            compute = 'circ.fft'
        else:
            compute = 'circ.' + method
    else:
        if method == 'auto':
            if K < np.log2(_dims(in1s, K, mode)):
                compute = 'direct'
            else:
                compute = 'scipy_convolve'
        else:
            compute = method

    if compute == 'direct':
        try:
            import numba  # noqa: F401
        except ImportError:
            warn("Did not find Numba, switch to 'scipy_convolve'.")
            compute = 'scipy_convolve'

    # Check which method is asked for
    if compute == 'direct':
        C = _direct(in1s, in2, mode, disable_jit, workers)
    elif compute == 'toeplitz':
        C = _toeplitz(in1s, in2, mode, workers)
    elif compute == 'scipy_convolve':
        C = _scipy_encapsulation(in1s, in2, mode, workers)
    elif compute == 'oa':
        C = _oaconvolve(in1s, in2, mode=mode, workers=workers)
    elif 'circ.' in compute:
        C = _circconvolve(in1s, in2,
                          method.replace('circ.', ''), disable_jit, workers)
    else:
        raise ValueError("method is not in " + str(methods))

    L = LazyLinOp(
        shape=C.shape,
        matmat=lambda x: (
            C @ x if _is_cplx(x.dtype, in2.dtype)
            else np.real(C @ x)
        ),
        rmatmat=lambda x: (
            C.H @ x if _is_cplx(x.dtype, in2.dtype)
            else np.real(C.H @ x)
        ),
        dtype=in2.dtype
    )
    # for callee information
    L.disable_jit = disable_jit
    return L


def _direct(in1s: int, in2: np.ndarray,
            mode: str = 'full', disable_jit: int = 0, workers=None):
    r"""Builds a :class:`.LazyLinOp` for the convolution of
    a signal of size ``in1s`` with a kernel ``in2``.
    If shape of the input array is ``(in1s, batch)``,
    return convolution per column.
    Function uses direct computation: nested for loops.
    You can switch on Numba jit and enable ``prange``.
    Larger the signal is better the performances are.
    Larger the batch size is better the performances are.
    Do not call ``_direct`` function outside
    of ``convolve`` function.

    Args:
        in1s: ``int``
            Length of the input.
        in2: ``np.ndarray``
            Kernel to convolve with the signal, shape is ``(K, )``.
        mode: ``str``, optional

            - 'full' computes convolution (input + padding).
            - 'valid' computes 'full' mode and extract centered output that
              does not depend on the padding.
            - 'same' computes 'full' mode and extract centered output that has
              the same shape that the input.
        disable_jit: ``int``, optional
            If 0 (default) enable Numba jit.
            It only matters for ``method='direct'``.
            Be careful that ``method='direct'`` is very slow
            when Numba jit is disabled.
            Prefix by ``NUMBA_NUM_THREADS=$t`` to launch ``t`` threads.

    Returns:
        :class:`.LazyLinOp`
    """

    # convolve function already checked for Numba.
    # Therefore, no need of try ... except ... here.
    import numba as nb
    from numba import njit, prange
    nb.config.THREADING_LAYER = 'omp'
    nb.config.DISABLE_JIT = disable_jit
    if workers is not None and 'NUMBA_NUM_THREADS' not in os.environ:
        nb.config.NUMBA_NUM_THREADS = workers

    K = in2.shape[0]
    M = (
        (in1s + K - 1) * int(mode == 'full') +
        (in1s - K + 1) * int(mode == 'valid') +
        in1s * int(mode == 'same')
    )
    P = (
        (in1s - K + 1) * int(mode == 'full') +
        (in1s + K - 1) * int(mode == 'valid') +
        in1s * int(mode == 'same')
    )
    start = (in1s + K - 1 - M) // 2
    rstart = (in1s + K - 1 - P) // 2

    @njit(parallel=True, cache=True)
    def _matmat(x, kernel):

        K = kernel.shape[0]
        batch_size = x.shape[1]
        y = np.full((M, batch_size),
                    0.0 * (kernel[0] * x[0, 0]))
        # y[n] = sum(h[k] * x[n - k], k, 0, K - 1)
        # n - k > 0 and n - k < len(x)
        for i in prange(start, start + M):
            # i - j >= 0
            # i - j < in1s
            for j in range(
                    min(max(0, i - in1s + 1), K),
                    min(K, i + 1)
            ):
                # NumPy (defaultly) uses row-major format
                for b in range(batch_size):
                    y[i - start, b] += kernel[j] * x[i - j, b]
        return y

    @njit(parallel=True, cache=True)
    def _rmatmat(x, kernel):

        K = kernel.shape[0]
        S, batch_size = x.shape
        y = np.full((in1s, batch_size), 0.0 * (kernel[0] * x[0, 0]))
        # y[n] = sum(h[k] * x[k + n], k, 0, K - 1)
        # k + n < len(x)
        for i in prange(rstart, rstart + in1s):
            for j in range(min(max(0, i - S + 1), K),
                           min(K, i + 1)):
                # NumPy (defaultly) uses row-major format
                for b in range(batch_size):
                    y[in1s + rstart - i - 1, b] += np.conjugate(
                        kernel[j]) * x[j - i + S - 1, b]
        return y

    return LazyLinOp(
        shape=(M, in1s),
        matmat=lambda x: _matmat(x, in2),
        rmatmat=lambda x: _rmatmat(x, in2)
    )


def _toeplitz(in1s: int, in2: np.ndarray, mode: str = 'full',
              workers: int = None):
    r"""Builds a :class:`.LazyLinOp` for the convolution of
    a signal of size ``in1s`` with a kernel ``in2``.
    If shape of the input array is ``(in1s, batch)``,
    return convolution per column.
    Function uses ``scipy.linalg.toeplitz`` or ``scipy.linalg.matmul_toeplitz``
    implementation to compute convolution.
    Do not call ``_toeplitz`` function outside
    of ``convolve`` function.

    Args:
        in1s: ``int``
            Length of the input.
        in2: ``np.ndarray``
            Kernel to convolve with the signal, shape is ``(K, )``.
        mode: ``str``, optional

            - 'full' computes convolution (input + padding).
            - 'valid' computes 'full' mode and extract centered output that
              does not depend on the padding.
            - 'same' computes 'full' mode and extract centered output that has
              the same shape that the input.
        workers:
            See convolve().
            Used only for matmul_toeplitz (if in1s > 2048).
            Can be overridden by OMP_NUM_THREADS environment variable.

    Returns:
        :class:`.LazyLinOp`
    """

    K = in2.shape[0]
    M = _dims(in1s, K, mode)
    i0 = (in1s + K - 1 - M) // 2

    if mode == 'full':
        # No need to slice rows
        c = np.pad(in2, (0, in1s - 1))
        r = np.pad([in2[0]], (0, in1s - 1))
    else:
        # Slice rows of the Toeplitz matrix
        if in2[i0:].shape[0] > M:
            # Handle the case such that kernel length
            # is bigger than signal length.
            c = np.copy(in2[i0:(i0 + M)])
        else:
            c = np.pad(in2[i0:], (0, M - (K - i0)))
        if in2[:(i0 + 1)].shape[0] > in1s:
            # Handle the case such that kernel length
            # is bigger than signal length.
            r = np.flip(in2[(i0 + 1 - in1s):(i0 + 1)])
        else:
            r = np.pad(np.flip(in2[:(i0 + 1)]), (0, in1s - (i0 + 1)))

    tmp = "OMP_NUM_THREADS"
    workers = (
        int(os.environ[tmp]) if tmp in os.environ.keys()
        else (-1 if workers is None else workers)
    )

    def _mat(c, r, x):
        if in1s < 2048:
            return sp.linalg.toeplitz(c, r) @ x
        else:
            return sp.linalg.matmul_toeplitz(
                (c, r), x,
                check_finite=False, workers=workers)

    # Convolution Toeplitz matrix is lower triangular,
    # therefore we have toeplitz(c, r).T = toeplitz(r, c)
    return LazyLinOp(
        shape=(_dims(in1s, K, mode), _dims(in1s, K, 'same')),
        matmat=lambda x: _mat(c, r, x),
        rmatmat=lambda x: _mat(r.conj(), c.conj(), x),
        dtype=in2.dtype
    )


def _scipy_encapsulation(in1s: int, in2: np.ndarray, mode: str = 'full',
                         workers=None):
    r"""Builds a :class:`.LazyLinOp` for the convolution of
    a signal of size ``in1s`` with a kernel ``in2``.
    If shape of the input array is ``(in1s, batch)``,
    return convolution per column.
    Function uses encapsulation of ``scipy.signal.convolve``
    to compute convolution.
    Do not call ``_scipy_encapsulation`` function outside
    of ``convolve`` function.

    Args:
        in1s: ``int``
            Length of the input.
        in2: ``np.ndarray``
            Kernel to convolve with the signal, shape is ``(K, )``.
        mode: ``str``, optional

            - 'full' computes convolution (input + padding).
            - 'valid' computes 'full' mode and extract centered output that
              does not depend on the padding.
            - 'same' computes 'full' mode and extract centered output that has
              the same shape that the input.
        workers:
            See convolve().
            Can be overridden by OMP_NUM_THREADS environment variable.

    Returns:
        :class:`.LazyLinOp`
    """

    # Length of the output as a function of convolution mode
    K = in2.shape[0]
    tmp = "OMP_NUM_THREADS"
    workers = (
        int(os.environ[tmp]) if tmp in os.environ.keys()
        else (-1 if workers is None else workers)
    )

    def _matmat(x):
        # x is always 2d
        batch_size = x.shape[1]
        y = np.empty((_dims(in1s, K, mode), batch_size),
                     dtype=(x[0, 0] * in2[0]).dtype)
        with sp.fft.set_workers(workers):
            for b in range(batch_size):
                y[:, b] = sp.signal.convolve(x[:, b],
                                             in2, mode=mode,
                                             method='auto')
        return y

    def _rmatmat(x):
        # x is always 2d
        batch_size = x.shape[1]
        y = np.empty((_dims(in1s, K, 'same'), batch_size),
                     dtype=(x[0, 0] * in2[0]).dtype)
        with sp.fft.set_workers(workers):
            for b in range(batch_size):
                y[:, b] = np.flip(
                    sp.signal.convolve(np.flip(x[:, b]),
                                       in2,
                                       mode=_rmode(mode),
                                       method='auto')
                )
        return y

    return LazyLinOp(
        shape=(_dims(in1s, K, mode), _dims(in1s, K, 'same')),
        matmat=lambda x: _matmat(x),
        rmatmat=lambda x: _rmatmat(x),
        dtype=in2.dtype
    )


def _oaconvolve(in1s: int, in2: np.ndarray, mode: str = 'full',
                workers: int = None):
    """This function implements overlap-add method for convolution.
    Builds a :class:`.LazyLinOp` for the convolution
    of a signal of length ``in1s`` with the kernel ``in2``.
    Do not call ``_oaconvolve`` function outside of ``convolve`` function.

    Args:
        in1s: ``int``
            Length of the input.
        in2: ``np.ndarray``
            Kernel to use for the convolution.
        mode: ``str``, optional

            - 'full' computes convolution (input + padding).
            - 'valid' computes 'full' mode and extract centered
              output that does not depend on the padding.
            - 'same' computes 'full' mode and extract centered
              output that has the same shape that the input.
        workers:
            see convolve().
            Can be overridden by OMP_NUM_THREADS environment variable.

    Returns:
        :class:`.LazyLinOp`
    """

    tmp = "OMP_NUM_THREADS"
    workers = (
        int(os.environ[tmp]) if tmp in os.environ.keys()
        else (os.cpu_count() if workers is None else workers)
    )

    # Size of the kernel
    K = in2.shape[0]
    # Size of the output (full mode)
    Y = in1s + K - 1

    # Block size B, number of blocks X = in1s / B
    B = K
    while B < min(in1s, K) or not is_power_of_two(B):
        B += 1

    # Number of blocks
    step = B
    B *= 2
    R = in1s % step
    X = in1s // step + 1 if R > 0 else in1s // step

    # Create LazyLinOp C that will be applied to all the blocks.
    # Use mpad to pad each block.
    DFT = fft(B, norm=None, workers=workers)
    if in1s > (2 * K):
        # If the signal size is greater than twice
        # the size of the kernel use overlap-based convolution
        D = diag(DFT @ eye(B, n=K, k=0) @ in2, k=0)
        F = DFT.inv() @ D @ DFT
        # block_diag(*[F] * X) is equivalent to kron(eye, F)
        C = oa(B, X, overlap=B - step) @ block_diag(*[F] * X) \
            @ mpad2(step, X, n=B - step)
        if (X * step) > in1s:
            C = C @ eye(X * step, n=in1s, k=0)
    else:
        # If the signal size is not greater than twice
        # the size of the kernel use FFT-based convolution
        F = fft(Y, norm=None, workers=workers)
        D = diag(F @ eye(Y, n=K, k=0) @ in2, k=0)
        C = F.inv() @ D @ F @ eye(Y, n=in1s, k=0)

    # Convolution mode
    if mode == 'valid' or mode == 'same':
        if mode == 'valid':
            # Compute full mode, valid mode returns
            # elements that do not depend on the padding.
            extract = in1s - K + 1
        else:
            # Keep the middle of full mode (centered)
            # and returns the same size that the signal size.
            extract = in1s
        start = (Y - extract) // 2
    else:
        extract, start = Y, 0
    # Use eye operator to extract
    return eye(extract, n=C.shape[0], k=start) @ C


def _circconvolve(in1s: int, in2: np.ndarray,
                  method: str = 'auto', disable_jit: int = 0,
                  workers: int = None):
    """Builds a :class:`.LazyLinOp` for the circular convolution.
    Do not call ``_circconvolve`` function outside of ``convolve`` function.

    Args:
        in1s: ``int``
            Length of the input.
        in2: ``np.ndarray``
            Kernel to use for the convolution.
        method: ``str``, optional

            - 'auto' use best implementation.
            - 'direct' direct computation using
              nested for loops (Numba implementation).
              Larger the batch is better the performances are.
            - 'fft' use SciPy encapsulation of the FFT.
        disable_jit: int, optional
            If 0 (default) enable Numba jit.
        workers:
            see convolve().
            Used only if method not 'direct' and in2 shape smaller
            than log2(in1s).
            Can be overridden by OMP_NUM_THREADS environment variable.

    Returns:
        :class:`.LazyLinOp`
    """

    tmp = method
    try:
        import numba as nb
        from numba import njit, prange
        nb.config.THREADING_LAYER = 'omp'
        nb.config.DISABLE_JIT = disable_jit
        if workers is not None and 'NUMBA_NUM_THREADS' not in os.environ:
            nb.config.NUMBA_NUM_THREADS = workers
    except ImportError:
        if tmp == 'direct':
            warn("Did not find Numba, switch to fft.")
            tmp = 'fft'

    if tmp == 'direct' or (tmp == 'auto' and in2.shape[0] < np.log2(in1s)):

        @njit(parallel=True, cache=True)
        def _matmat(kernel, signal):
            K = kernel.shape[0]
            B = signal.shape[1]
            y = np.full((in1s, B), 0.0 * (kernel[0] * signal[0, 0]))
            # y[n] = sum(h[k] * s[n - k mod N], k, 0, K - 1)
            for i in prange(in1s):
                # Split the loop to avoid computation of ``np.mod``.
                for j in range(min(K, i + 1)):
                    # NumPy uses row-major format
                    for b in range(B):
                        y[i, b] += (
                            kernel[j] * signal[i - j, b]
                        )
                for j in range(i + 1, K, 1):
                    # NumPy uses row-major format
                    for b in range(B):
                        y[i, b] += (
                            kernel[j] * signal[in1s + i - j, b]
                        )
            return y

        @njit(parallel=True, cache=True)
        def _rmatmat(kernel, signal):
            K = kernel.shape[0]
            B = signal.shape[1]
            y = np.full((in1s, B), 0.0 * (kernel[0] * signal[0, 0]))
            # y[n] = sum(h[k] * s[k + n mod N], k, 0, K - 1)
            for i in prange(in1s):
                # Split the loop to avoid computation of ``np.mod``.
                for j in range(min(K, in1s - i)):
                    # NumPy uses row-major format
                    for b in range(B):
                        y[i, b] += (
                            np.conjugate(kernel[j]) * signal[i + j, b]
                        )
                for j in range(min(K, in1s - i), K, 1):
                    # NumPy uses row-major format
                    for b in range(B):
                        y[i, b] += (
                            np.conjugate(kernel[j]) * signal[i + j - in1s, b]
                        )
            return y

        return LazyLinOp(
            shape=(in1s, in1s),
            matmat=lambda x: _matmat(in2, x),
            rmatmat=lambda x: _rmatmat(in2, x)
        )
    else:
        key = "OMP_NUM_THREADS"
        workers = (
            int(os.environ[key]) if key in os.environ.keys()
            else (os.cpu_count() if workers is None else workers)
        )
        # Zero-pad the kernel
        pin2 = np.pad(in2, (0, in1s - in2.shape[0]),
                      mode='constant', constant_values=0.0)
        # Op = FFT^-1 @ diag(FFT(kernel)) @ FFT
        D = diag(fft(in1s, norm=None, workers=workers) @ pin2, k=0)
        return fft(in1s, norm='1/n', workers=workers).H @ D \
            @ fft(in1s, norm=None, workers=workers)


# if __name__ == '__main__':
#     import doctest
#     doctest.testmod()
