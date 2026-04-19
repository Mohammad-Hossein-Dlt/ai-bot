
from src.domain.enums import AiActionType, AiPlatformType
from src.models.schemas.category.create_category_input import CreateCategoryInput

content_creation_google = [
    CreateCategoryInput(
        ai_action_type=AiActionType.content_creation,
        ai_platform_type=AiPlatformType.google,
        slug="gemini-3.1-pro-preview",
        name="Gemini 3.1 Pro preview",
        tokens=10,
    ),
    CreateCategoryInput(
        ai_action_type=AiActionType.content_creation,
        ai_platform_type=AiPlatformType.google,
        slug="gemini-3.1-flash-lite-preview",
        name="Gemini 3.1 Flash lite preview",
        tokens=10,
    ),
    CreateCategoryInput(
        ai_action_type=AiActionType.content_creation,
        ai_platform_type=AiPlatformType.google,
        slug="gemini-3-flash-preview",
        name="Gemini 3 Flash preview",
        tokens=10,
    ),
    CreateCategoryInput(
        ai_action_type=AiActionType.content_creation,
        ai_platform_type=AiPlatformType.google,
        slug="gemini-2.5-pro",
        name="Gemini 2.5 Pro",
        tokens=10,
    ),
    CreateCategoryInput(
        ai_action_type=AiActionType.content_creation,
        ai_platform_type=AiPlatformType.google,
        slug="gemini-2.5-flash",
        name="Gemini 2.5 Flash",
        tokens=10,
    ),
    CreateCategoryInput(
        ai_action_type=AiActionType.content_creation,
        ai_platform_type=AiPlatformType.google,
        slug="gemini-2.5-flash-lite",
        name="Gemini 2.5 Flash lite",
        tokens=10,
    ),
    CreateCategoryInput(
        ai_action_type=AiActionType.content_creation,
        ai_platform_type=AiPlatformType.google,
        slug="gemini-flash-lite-latest",
        name="Gemini Flash lite latest",
        tokens=10,
    ),
]

content_creation_open_ai = [
    CreateCategoryInput(
        ai_action_type=AiActionType.content_creation,
        ai_platform_type=AiPlatformType.open_ai,
        slug="gpt-5.4",
        name="Gpt 5.4",
        tokens=10,
    ),
    CreateCategoryInput(
        ai_action_type=AiActionType.content_creation,
        ai_platform_type=AiPlatformType.open_ai,
        slug="gpt-5.2-pro",
        name="Gpt 5.2 pro",
        tokens=10,
    ),
    CreateCategoryInput(
        ai_action_type=AiActionType.content_creation,
        ai_platform_type=AiPlatformType.open_ai,
        slug="gpt-5.2-chat-latest",
        name="Gpt 5.2 chat latest",
        tokens=10,
    ),
    CreateCategoryInput(
        ai_action_type=AiActionType.content_creation,
        ai_platform_type=AiPlatformType.open_ai,
        slug="gpt-5.2",
        name="Gpt 5.2",
        tokens=10,
    ),
    CreateCategoryInput(
        ai_action_type=AiActionType.content_creation,
        ai_platform_type=AiPlatformType.open_ai,
        slug="gpt-4.1",
        name="Gpt 4.1",
        tokens=10,
    ),
    CreateCategoryInput(
        ai_action_type=AiActionType.content_creation,
        ai_platform_type=AiPlatformType.open_ai,
        slug="gpt-4.1-mini",
        name="Gpt 4.1 mini",
        tokens=10,
    ),
    CreateCategoryInput(
        ai_action_type=AiActionType.content_creation,
        ai_platform_type=AiPlatformType.open_ai,
        slug="gpt-4.1-nano",
        name="Gpt 4.1 nano",
        tokens=10,
    ),
    CreateCategoryInput(
        ai_action_type=AiActionType.content_creation,
        ai_platform_type=AiPlatformType.open_ai,
        slug="chatgpt-4o-latest",
        name="Chatgpt 4o latest",
        tokens=10,
    ),
    CreateCategoryInput(
        ai_action_type=AiActionType.content_creation,
        ai_platform_type=AiPlatformType.open_ai,
        slug="gpt-4o",
        name="Gpt 4o",
        tokens=10,
    ),
    CreateCategoryInput(
        ai_action_type=AiActionType.content_creation,
        ai_platform_type=AiPlatformType.open_ai,
        slug="gpt-4o-mini",
        name="Gpt 4o mini",
        tokens=10,
    ),
    CreateCategoryInput(
        ai_action_type=AiActionType.content_creation,
        ai_platform_type=AiPlatformType.open_ai,
        slug="o4-mini",
        name="O4 mini",
        tokens=10,
    ),
    CreateCategoryInput(
        ai_action_type=AiActionType.content_creation,
        ai_platform_type=AiPlatformType.open_ai,
        slug="o3",
        name="O3",
        tokens=10,
    ),
    CreateCategoryInput(
        ai_action_type=AiActionType.content_creation,
        ai_platform_type=AiPlatformType.open_ai,
        slug="o3-mini",
        name="O3 mini",
        tokens=10,
    ),
    CreateCategoryInput(
        ai_action_type=AiActionType.content_creation,
        ai_platform_type=AiPlatformType.open_ai,
        slug="o3-mini-high",
        name="O3 mini high",
        tokens=10,
    ),
    CreateCategoryInput(
        ai_action_type=AiActionType.content_creation,
        ai_platform_type=AiPlatformType.open_ai,
        slug="o3-mini-low",
        name="O3 mini low",
        tokens=10,
    ),
    CreateCategoryInput(
        ai_action_type=AiActionType.content_creation,
        ai_platform_type=AiPlatformType.open_ai,
        slug="o1",
        name="O1",
        tokens=10,
    ),
    CreateCategoryInput(
        ai_action_type=AiActionType.content_creation,
        ai_platform_type=AiPlatformType.open_ai,
        slug="o1-mini",
        name="O1 mini",
        tokens=10,
    ),
]

text_to_image_google = [
    CreateCategoryInput(
        ai_action_type=AiActionType.text_to_image,
        ai_platform_type=AiPlatformType.google,
        slug="gemini-3.1-flash-image-preview",
        name="Nano Banana 2",
        tokens=10,
    ),
    CreateCategoryInput(
        ai_action_type=AiActionType.text_to_image,
        ai_platform_type=AiPlatformType.google,
        slug="gemini-3-pro-image-preview",
        name="Nano Banana Pro",
        tokens=10,
    ),
    CreateCategoryInput(
        ai_action_type=AiActionType.text_to_image,
        ai_platform_type=AiPlatformType.google,
        slug="gemini-2.5-flash-image-preview",
        name="Nano Banana 1",
        tokens=10,
    ),
]

text_to_image_open_ai = [
    CreateCategoryInput(
        ai_action_type=AiActionType.text_to_image,
        ai_platform_type=AiPlatformType.open_ai,
        slug="gpt-image-1",
        name="Gpt image 1",
        tokens=10,
    ),
    CreateCategoryInput(
        ai_action_type=AiActionType.text_to_image,
        ai_platform_type=AiPlatformType.open_ai,
        slug="gpt-image-1-mini",
        name="Gpt image 1 mini",
        tokens=10,
    ),
    CreateCategoryInput(
        ai_action_type=AiActionType.text_to_image,
        ai_platform_type=AiPlatformType.open_ai,
        slug="dall-e-2",
        name="Dall e 2",
        tokens=10,
    ),
    CreateCategoryInput(
        ai_action_type=AiActionType.text_to_image,
        ai_platform_type=AiPlatformType.open_ai,
        slug="dall-e-3",
        name="Dall e 3",
        tokens=10,
    ),
]

text_to_audio_google = [
    CreateCategoryInput(
        ai_action_type=AiActionType.text_to_audio,
        ai_platform_type=AiPlatformType.google,
        slug="gemini-2.5-flash-preview-tts",
        name="Gemini 2.5 flash preview tts",
        tokens=10,
    ),
    CreateCategoryInput(
        ai_action_type=AiActionType.text_to_audio,
        ai_platform_type=AiPlatformType.google,
        slug="gemini-2.5-pro-preview-tts",
        name="Gemini 2.5 pro preview tts",
        tokens=10,
    ),
]

text_to_audio_open_ai = [
    CreateCategoryInput(
        ai_action_type=AiActionType.text_to_audio,
        ai_platform_type=AiPlatformType.open_ai,
        slug="tts-1-hd",
        name="tts 1 hd",
        tokens=10,
    ),
    CreateCategoryInput(
        ai_action_type=AiActionType.text_to_audio,
        ai_platform_type=AiPlatformType.open_ai,
        slug="tts-1",
        name="tts 1",
        tokens=10,
    ),
    CreateCategoryInput(
        ai_action_type=AiActionType.text_to_audio,
        ai_platform_type=AiPlatformType.open_ai,
        slug="gpt-4o-mini-tts",
        name="gpt 4o mini tts",
        tokens=10,
    ),
]

audio_to_text_google = []

audio_to_text_open_ai = [
    CreateCategoryInput(
        ai_action_type=AiActionType.audio_to_text,
        ai_platform_type=AiPlatformType.open_ai,
        slug="whisper-1",
        name="whisper 1",
        tokens=10,
    ),
]

all_categories = [
    
    *content_creation_google,
    *content_creation_open_ai,
    
    *text_to_image_google,
    *text_to_image_open_ai,
    
    *text_to_audio_google,
    *text_to_audio_open_ai,
    
    *audio_to_text_google,
    *audio_to_text_open_ai,
]