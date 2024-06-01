# License: MIT
# Copyright © 2022 Frequenz Energy-as-a-Service GmbH

"""Exceptions raised by the microgrid API client."""

from __future__ import annotations

from typing import Protocol

import grpclib


class ClientError(Exception):
    """There was an error in the microgrid API client.

    To simplify retrying, errors are classified as
    [retryable][frequenz.client.microgrid.ClientError.is_retryable], or not. Retryable
    errors might succeed if retried, while permanent errors won't. When uncertain,
    errors are assumed to be retryable.
    """

    def __init__(
        self,
        *,
        server_url: str,
        operation: str,
        description: str,
        retryable: bool,
    ) -> None:
        """Create a new instance.

        Args:
            server_url: The URL of the server that returned the error.
            operation: The operation that caused the error.
            description: A human-readable description of the error.
            retryable: Whether retrying the operation might succeed.
        """
        super().__init__(
            f"Failed calling {operation!r} on {server_url!r}: {description}"
        )

        self.server_url = server_url
        """The URL of the server that returned the error."""

        self.operation = operation
        """The operation that caused the error."""

        self.description = description
        """The human-readable description of the error."""

        self.is_retryable = retryable
        """Whether retrying the operation might succeed."""

    @classmethod
    def from_grpc_error(
        cls,
        *,
        server_url: str,
        operation: str,
        grpc_error: grpclib.GRPCError,
    ) -> GrpcError:
        """Create an instance of the appropriate subclass from a gRPC error.

        Args:
            server_url: The URL of the server that returned the error.
            operation: The operation that caused the error.
            grpc_error: The gRPC error to convert.

        Returns:
            An instance of
                [GrpcError][frequenz.client.microgrid.GrpcError] if
                the gRPC status is not recognized, or an appropriate subclass if it is.
        """

        class Ctor(Protocol):
            """A protocol for the constructor of a subclass of `GrpcError`."""

            def __call__(
                self, *, server_url: str, operation: str, grpc_error: grpclib.GRPCError
            ) -> GrpcError: ...

        status_map: dict[grpclib.Status, Ctor] = {
            grpclib.Status.CANCELLED: OperationCancelled,
            grpclib.Status.UNKNOWN: UnknownError,
            grpclib.Status.INVALID_ARGUMENT: InvalidArgument,
            grpclib.Status.DEADLINE_EXCEEDED: OperationTimedOut,
            grpclib.Status.NOT_FOUND: EntityNotFound,
            grpclib.Status.ALREADY_EXISTS: EntityAlreadyExists,
            grpclib.Status.PERMISSION_DENIED: PermissionDenied,
            grpclib.Status.RESOURCE_EXHAUSTED: ResourceExhausted,
            grpclib.Status.FAILED_PRECONDITION: OperationPreconditionFailed,
            grpclib.Status.ABORTED: OperationAborted,
            grpclib.Status.OUT_OF_RANGE: OperationOutOfRange,
            grpclib.Status.UNIMPLEMENTED: OperationNotImplemented,
            grpclib.Status.INTERNAL: InternalError,
            grpclib.Status.UNAVAILABLE: ServiceUnavailable,
            grpclib.Status.DATA_LOSS: DataLoss,
            grpclib.Status.UNAUTHENTICATED: OperationUnauthenticated,
        }

        if ctor := status_map.get(grpc_error.status):
            return ctor(
                server_url=server_url, operation=operation, grpc_error=grpc_error
            )
        return UnrecognizedGrpcStatus(
            server_url=server_url,
            operation=operation,
            grpc_error=grpc_error,
        )


class GrpcError(ClientError):
    """The gRPC server returned an error with a status code.

    These errors are specific to gRPC. If you want to use the client in
    a protocol-independent way, you should avoid catching this exception. Catching
    subclasses that don't have *grpc* in their name should be protocol-independent.

    References:
        * [gRPC status
           codes](https://github.com/grpc/grpc/blob/master/doc/statuscodes.md)
    """

    def __init__(  # pylint: disable=too-many-arguments
        self,
        *,
        server_url: str,
        operation: str,
        description: str,
        grpc_error: grpclib.GRPCError,
        retryable: bool,
    ) -> None:
        """Create a new instance.

        Args:
            server_url: The URL of the server that returned the error.
            operation: The operation that caused the error.
            description: A human-readable description of the error.
            grpc_error: The gRPC error originating this exception.
            retryable: Whether retrying the operation might succeed.
        """
        message = f": {grpc_error.message}" if grpc_error.message else ""
        details = f" ({grpc_error.details})" if grpc_error.details else ""
        super().__init__(
            server_url=server_url,
            operation=operation,
            description=f"{description} <status={grpc_error.status.name}>{message}{details}",
            retryable=retryable,
        )
        self.description = description

        self.grpc_error = grpc_error
        """The original gRPC error."""


class UnrecognizedGrpcStatus(GrpcError):
    """The gRPC server returned an unrecognized status code."""

    def __init__(
        self, *, server_url: str, operation: str, grpc_error: grpclib.GRPCError
    ) -> None:
        """Create a new instance.

        Args:
            server_url: The URL of the server that returned the error.
            operation: The operation that caused the error.
            grpc_error: The gRPC error originating this exception.
        """
        super().__init__(
            server_url=server_url,
            operation=operation,
            description="Got an unrecognized status code",
            grpc_error=grpc_error,
            retryable=True,  # We don't know so we assume it's retryable
        )


class OperationCancelled(GrpcError):
    """The operation was cancelled."""

    def __init__(
        self, *, server_url: str, operation: str, grpc_error: grpclib.GRPCError
    ) -> None:
        """Create a new instance.

        Args:
            server_url: The URL of the server that returned the error.
            operation: The operation that caused the error.
            grpc_error: The gRPC error originating this exception.
        """
        super().__init__(
            server_url=server_url,
            operation=operation,
            description="The operation was cancelled",
            grpc_error=grpc_error,
            retryable=True,
        )


class UnknownError(GrpcError):
    """There was an error that can't be described using other statuses."""

    def __init__(
        self, *, server_url: str, operation: str, grpc_error: grpclib.GRPCError
    ) -> None:
        """Create a new instance.

        Args:
            server_url: The URL of the server that returned the error.
            operation: The operation that caused the error.
            grpc_error: The gRPC error originating this exception.
        """
        super().__init__(
            server_url=server_url,
            operation=operation,
            description="There was an error that can't be described using other statuses",
            grpc_error=grpc_error,
            retryable=True,  # We don't know so we assume it's retryable
        )


class InvalidArgument(GrpcError, ValueError):
    """The client specified an invalid argument.

    Note that this error differs from
    [OperationPreconditionFailed][frequenz.client.microgrid.OperationPreconditionFailed].
    This error indicates arguments that are problematic regardless of the state of the
    system (e.g., a malformed file name).
    """

    def __init__(
        self, *, server_url: str, operation: str, grpc_error: grpclib.GRPCError
    ) -> None:
        """Create a new instance.

        Args:
            server_url: The URL of the server that returned the error.
            operation: The operation that caused the error.
            grpc_error: The gRPC error originating this exception.
        """
        super().__init__(
            server_url=server_url,
            operation=operation,
            description="The client specified an invalid argument",
            grpc_error=grpc_error,
            retryable=False,
        )


class OperationTimedOut(GrpcError):
    """The time limit was exceeded while waiting for the operationt o complete.

    For operations that change the state of the system, this error may be returned even
    if the operation has completed successfully. For example, a successful response from
    a server could have been delayed long.
    """

    def __init__(
        self, *, server_url: str, operation: str, grpc_error: grpclib.GRPCError
    ) -> None:
        """Create a new instance.

        Args:
            server_url: The URL of the server that returned the error.
            operation: The operation that caused the error.
            grpc_error: The gRPC error originating this exception.
        """
        super().__init__(
            server_url=server_url,
            operation=operation,
            description="The time limit was exceeded while waiting for the operation "
            "to complete",
            grpc_error=grpc_error,
            retryable=True,
        )


class EntityNotFound(GrpcError):
    """The requested entity was not found.

    Note that this error differs from
    [PermissionDenied][frequenz.client.microgrid.PermissionDenied]. This error is
    used when the requested entity is not found, regardless of the user's permissions.
    """

    def __init__(
        self, *, server_url: str, operation: str, grpc_error: grpclib.GRPCError
    ) -> None:
        """Create a new instance.

        Args:
            server_url: The URL of the server that returned the error.
            operation: The operation that caused the error.
            grpc_error: The gRPC error originating this exception.
        """
        super().__init__(
            server_url=server_url,
            operation=operation,
            description="The requested entity was not found",
            grpc_error=grpc_error,
            retryable=True,  # If the entity is added later it might succeed
        )


class EntityAlreadyExists(GrpcError):
    """The entity that we attempted to create already exists."""

    def __init__(
        self, *, server_url: str, operation: str, grpc_error: grpclib.GRPCError
    ) -> None:
        """Create a new instance.

        Args:
            server_url: The URL of the server that returned the error.
            operation: The operation that caused the error.
            grpc_error: The gRPC error originating this exception.
        """
        super().__init__(
            server_url=server_url,
            operation=operation,
            description="The entity that we attempted to create already exists",
            grpc_error=grpc_error,
            retryable=True,  # If the entity is deleted later it might succeed
        )


class PermissionDenied(GrpcError):
    """The caller does not have permission to execute the specified operation.

    Note that when the operation is rejected due to other reasons, such as the resources
    being exhausted or the user not being authenticated at all, different errors should
    be catched instead
    ([ResourceExhausted][frequenz.client.microgrid.ResourceExhausted] and
    [OperationUnauthenticated][frequenz.client.microgrid.OperationUnauthenticated]
     respectively).
    """

    def __init__(
        self, *, server_url: str, operation: str, grpc_error: grpclib.GRPCError
    ) -> None:
        """Create a new instance.

        Args:
            server_url: The URL of the server that returned the error.
            operation: The operation that caused the error.
            grpc_error: The gRPC error originating this exception.
        """
        super().__init__(
            server_url=server_url,
            operation=operation,
            description="The caller does not have permission to execute the specified "
            "operation",
            grpc_error=grpc_error,
            retryable=True,  # If the user is granted permission it might succeed
        )


class ResourceExhausted(GrpcError):
    """Some resource has been exhausted (for example per-user quota, disk space, etc.)."""

    def __init__(
        self, *, server_url: str, operation: str, grpc_error: grpclib.GRPCError
    ) -> None:
        """Create a new instance.

        Args:
            server_url: The URL of the server that returned the error.
            operation: The operation that caused the error.
            grpc_error: The gRPC error originating this exception.
        """
        super().__init__(
            server_url=server_url,
            operation=operation,
            description="Some resource has been exhausted (for example per-user quota, "
            "disk space, etc.)",
            grpc_error=grpc_error,
            retryable=True,  # If the resource is freed it might succeed
        )


class OperationPreconditionFailed(GrpcError):
    """The operation was rejected because the system is not in a required state.

    For example, the directory to be deleted is non-empty, an rmdir operation is applied
    to a non-directory, etc. The user should perform some corrective action before
    retrying the operation.
    """

    def __init__(
        self, *, server_url: str, operation: str, grpc_error: grpclib.GRPCError
    ) -> None:
        """Create a new instance.

        Args:
            server_url: The URL of the server that returned the error.
            operation: The operation that caused the error.
            grpc_error: The gRPC error originating this exception.
        """
        super().__init__(
            server_url=server_url,
            operation=operation,
            description="The operation was rejected because the system is not in a "
            "required state",
            grpc_error=grpc_error,
            retryable=True,  # If the system state changes it might succeed
        )


class OperationAborted(GrpcError):
    """The operation was aborted.

    Typically due to a concurrency issue or transaction abort.
    """

    def __init__(
        self, *, server_url: str, operation: str, grpc_error: grpclib.GRPCError
    ) -> None:
        """Create a new instance.

        Args:
            server_url: The URL of the server that returned the error.
            operation: The operation that caused the error.
            grpc_error: The gRPC error originating this exception.
        """
        super().__init__(
            server_url=server_url,
            operation=operation,
            description="The operation was aborted",
            grpc_error=grpc_error,
            retryable=True,
        )


class OperationOutOfRange(GrpcError):
    """The operation was attempted past the valid range.

    Unlike [InvalidArgument][frequenz.client.microgrid.InvalidArgument], this
    error indicates a problem that may be fixed if the system state changes.

    There is a fair bit of overlap with
    [OperationPreconditionFailed][frequenz.client.microgrid.OperationPreconditionFailed],
    this error is just a more specific version of that error and could be the result of
    an operation that doesn't even take any arguments.
    """

    def __init__(
        self, *, server_url: str, operation: str, grpc_error: grpclib.GRPCError
    ) -> None:
        """Create a new instance.

        Args:
            server_url: The URL of the server that returned the error.
            operation: The operation that caused the error.
            grpc_error: The gRPC error originating this exception.
        """
        super().__init__(
            server_url=server_url,
            operation=operation,
            description="The operation was attempted past the valid range",
            grpc_error=grpc_error,
            retryable=True,  # If the system state changes it might succeed
        )


class OperationNotImplemented(GrpcError):
    """The operation is not implemented or not supported/enabled in this service."""

    def __init__(
        self, *, server_url: str, operation: str, grpc_error: grpclib.GRPCError
    ) -> None:
        """Create a new instance.

        Args:
            server_url: The URL of the server that returned the error.
            operation: The operation that caused the error.
            grpc_error: The gRPC error originating this exception.
        """
        super().__init__(
            server_url=server_url,
            operation=operation,
            description="The operation is not implemented or not supported/enabled in "
            "this service",
            grpc_error=grpc_error,
            retryable=False,
        )


class InternalError(GrpcError):
    """Some invariants expected by the underlying system have been broken.

    This error code is reserved for serious errors.
    """

    def __init__(
        self, *, server_url: str, operation: str, grpc_error: grpclib.GRPCError
    ) -> None:
        """Create a new instance.

        Args:
            server_url: The URL of the server that returned the error.
            operation: The operation that caused the error.
            grpc_error: The gRPC error originating this exception.
        """
        super().__init__(
            server_url=server_url,
            operation=operation,
            description="Some invariants expected by the underlying system have been "
            "broken",
            grpc_error=grpc_error,
            retryable=True,  # If the system state changes it might succeed
        )


class ServiceUnavailable(GrpcError):
    """The service is currently unavailable.

    This is most likely a transient condition, which can be corrected by retrying with
    a backoff. Note that it is not always safe to retry non-idempotent operations.
    """

    def __init__(
        self, *, server_url: str, operation: str, grpc_error: grpclib.GRPCError
    ) -> None:
        """Create a new instance.

        Args:
            server_url: The URL of the server that returned the error.
            operation: The operation that caused the error.
            grpc_error: The gRPC error originating this exception.
        """
        super().__init__(
            server_url=server_url,
            operation=operation,
            description="The service is currently unavailable",
            grpc_error=grpc_error,
            retryable=True,  # If the service becomes available it might succeed
        )


class DataLoss(GrpcError):
    """Unrecoverable data loss or corruption."""

    def __init__(
        self, *, server_url: str, operation: str, grpc_error: grpclib.GRPCError
    ) -> None:
        """Create a new instance.

        Args:
            server_url: The URL of the server that returned the error.
            operation: The operation that caused the error.
            grpc_error: The gRPC error originating this exception.
        """
        super().__init__(
            server_url=server_url,
            operation=operation,
            description="Unrecoverable data loss or corruption",
            grpc_error=grpc_error,
            retryable=False,
        )


class OperationUnauthenticated(GrpcError):
    """The request does not have valid authentication credentials for the operation."""

    def __init__(
        self, *, server_url: str, operation: str, grpc_error: grpclib.GRPCError
    ) -> None:
        """Create a new instance.

        Args:
            server_url: The URL of the server that returned the error.
            operation: The operation that caused the error.
            grpc_error: The gRPC error originating this exception.
        """
        super().__init__(
            server_url=server_url,
            operation=operation,
            description="The request does not have valid authentication credentials "
            "for the operation",
            grpc_error=grpc_error,
            retryable=False,
        )
