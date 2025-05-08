START
Application
LOAD
configuration
from environment

INITIALIZE
web
server and register
route
` / `

DEFINE
route
` / `:
sessions ← load
all
sessions
from database ( or empty
list)
session_id ← get
`session_id`
from request args, or None
messages ← empty
list
error, notice, suggestion, chart_uri ← None

IF
request
method is POST:
file ← request.files['file']
CALL
handle_upload(file) → (error, notice, df)

IF
error is None:
rec ← recommend_chart(df)
raw_prompt ← build_raw_prompt(rec)
suggestion ← polish_prompt(raw_prompt)
chart_uri ← generate_chart_image(df, rec)
APPEND
user
message
to
messages: "Data Visualization of {file.name}"
APPEND
bot
message
to
messages: suggestion

RENDER
template
`index.html`
WITH
sessions, session_id, messages, error, notice, suggestion, chart_uri
END
route

RUN
server
