# What problem does this solve?
There is a problem with the way moonlight and sunshine interact when theres some latency (>100ms). If we rely on sunshine to draw the mouse cursor, any latency greater than ~100ms will immediately inform the user that there's "a lot" of lag. However, for all normal day to day use aside from gaming, this has very little actual effect on task productivity except causing significant psychological discomfort. 

Programs such as parsec appear to have very low input latency under such latecy regime because they do not draw the mouse cursor on the remote image but rather changes the local mouse cursor state to correspond to remote cursor.

This repo is a proof of concept to implement "mouse cursor state synchronization".

# How to run?
* Turn off remote cursor rendering using `Ctrl+shift+alt+N` and turn on local cursor rendering using `Ctrl+shift+alt+C` while in moonlight.
* From my testing it only works when under "borderless window" or "windowed" mode.
* first install requirements
    * `pip -r requirement.txt`
* on the server
    * `python server.py`
* on the client
    * edit `config.yaml` to change `serverip`
    * `python client.py`

# How does it work?
* Normally setting cursor state via win32 api is not possible globally and `SetCursor` only works for the current process. If we want to use another process to change cursor state of `Moonlight.exe` process, we would need to inject a dll and call the `SetCursor` function via that injected dll.
* This method in this repo bypasses this tricky issue by overwriting system level cursor state and tracking which process has window focus and restoring the system cursor state.
* Note: Moonlight(or sunshine) appears to have a bug where if you turn off remote cursor rendering via `Ctrl+shift+alt+N`, the cursor turns off except when it's in `IBEAM` state. This is the special text selector cursor. This cursor seems special because the way it is rendered is by inverting the pixels under the current cursor's pixels. Combined with the bug in moonlight, a double inversion will happen and would effectively make the cursor disappear. To avoid this, an empty system cursor is used when cursor state is `IBEAM` so only remote cursor will show up.
