The first character indicates the type of message and the rest is
message content according to `tank.proto` and encoded in base64.
#### Client -> Server message types
 - `0`: Movement
 - `1`: Voice
 - `2`: Nick Selection

#### Server -> Client message types
 - `0`: Info Broadcast
 - `1`: Voice
 - `2`: Init
 - `3`: Disconnect
 - `4`: Error Message
