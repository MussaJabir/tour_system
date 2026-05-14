import logging

from django.conf import settings

logger = logging.getLogger(__name__)


class AIServiceError(Exception):
    pass


def get_ai_response(prompt: str, system_prompt: str = '') -> str:
    from .models import AIConfiguration

    config = AIConfiguration.get_active()

    if config:
        api_key = config.api_key
        vendor = config.vendor
        model = config.model_name
        max_tokens = config.max_tokens
        temperature = float(config.temperature)
    else:
        api_key = settings.OPENAI_API_KEY
        vendor = 'openai'
        model = 'gpt-4o'
        max_tokens = 2000
        temperature = 0.7

    if not api_key:
        raise AIServiceError(
            'No AI API key configured. Go to Admin > AI Configuration to set one.'
        )

    try:
        if vendor == 'openai':
            return _call_openai(api_key, model, prompt, system_prompt, max_tokens, temperature)
        elif vendor == 'anthropic':
            return _call_anthropic(api_key, model, prompt, system_prompt, max_tokens)
        else:
            raise AIServiceError(f'Unknown vendor: {vendor}')
    except AIServiceError:
        raise
    except Exception as exc:
        logger.exception('AI API call failed')
        raise AIServiceError(str(exc)) from exc


def _call_openai(
    api_key: str,
    model: str,
    prompt: str,
    system_prompt: str,
    max_tokens: int,
    temperature: float,
) -> str:
    from openai import OpenAI

    client = OpenAI(api_key=api_key)
    messages = []
    if system_prompt:
        messages.append({'role': 'system', 'content': system_prompt})
    messages.append({'role': 'user', 'content': prompt})
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return response.choices[0].message.content


def _call_anthropic(
    api_key: str,
    model: str,
    prompt: str,
    system_prompt: str,
    max_tokens: int,
) -> str:
    from anthropic import Anthropic

    client = Anthropic(api_key=api_key)
    kwargs = {
        'model': model,
        'max_tokens': max_tokens,
        'messages': [{'role': 'user', 'content': prompt}],
    }
    if system_prompt:
        kwargs['system'] = system_prompt
    message = client.messages.create(**kwargs)
    return message.content[0].text
