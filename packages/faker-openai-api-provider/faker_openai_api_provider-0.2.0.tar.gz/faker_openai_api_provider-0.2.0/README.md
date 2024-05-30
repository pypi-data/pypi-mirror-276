# faker-openai-api-provider

Generate fake data that resembles fields in OpenAI API responses

> [!IMPORTANT]
> This ***does not*** generate fake AI responses/completions

## API

- `openai().chat.completion.id() -> str`
- `openai().file.id() -> str`
- `openai().beta.assistant.id() -> str`
- `openai().beta.thread.id() -> str`
- `openai().beta.thread.message.id() -> str`
- `openai().beta.thread.run.id() -> str`
- `openai().beta.thread.run.step.id() -> str`
- `openai().beta.thread.run.step.step_details.tool_call.id() -> str`

## Usage

```py
from faker import Faker
from faker_openai_api_provider import OpenAiApiProvider

fake = Faker()
fake.add_provider(OpenAiApiProvider)

chat_completion_id = fake.openai().chat.completion.id()
```

## Installation

```
pip install faker-openai-api-provider
```
