# Experimenting with GRPC

## Purpose

To see how GRPC handles channel status (liveliness and deadness).

## Setup

1. Install dependencies.

   ```bash
   $ pip install absl grpcio grpcio-tools 
   ```

2. Generate Python files from proto definition.

   ```bash
   $ python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. chat.proto
   ```

## Experiment

### Description

The channel between the client and the server is a unary_stream channel, i.e.
the client sends one request to the server, while the client sends a stream of
response to the client (in this case **3 responses**).

The server sleeps for **2 seconds** between every two responses.

### Commands

`$ python chat_server.py --port=50051` to start the server.

`$ python chat_client.py --port=50051` to start the client.

### Things to try out

1. Run server; run client, wait for it to finish normally; shutdown server.
2. Run client without server.

Observation:

```
RpcError: <_Rendezvous of RPC that terminated with (StatusCode.UNAVAILABLE, Connect Failed)>
```

3. Run server; run client; shutdown server after client receives the first message

Observation:

```
RpcError: <_Rendezvous of RPC that terminated with (StatusCode.INTERNAL, Received RST_STREAM with error code 2)>
```

4. Run server; run client; **suspend** server after client receives the first message

Observation: client freezes. Unable to shutdown with Ctrl-C

## Analogy

**Alice and Bob are talking on the phone.**

The phone company is keeping the connection alive. Alice and Bob get a
disconnection beep when the connection is down.

If Bob hangs up the phone, Alice hears a beep from the phone and she knows the 
connection is down, so she gives up. (Case 3)

However, if Bob went home without hanging the phone (because his dog is tearing 
down the sofa), the connection is still alive. Alice keeps waiting on the phone 
because she does not know that Bob left. (Case 4)

Alice is the client; Bob is the server; the phone company is GRPC.
