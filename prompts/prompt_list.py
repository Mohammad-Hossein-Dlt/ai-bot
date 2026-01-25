from . import (
    tone,
    words_length,
    article,
    contract,
    email,
    essay,
    fiction_story,
    letter,
    story,
    summarizing,
    video_production_scenario,
)

prompts = {
    "نامه": letter.prompt,
    "ایمیل": email.prompt,
    "قرارداد": contract.prompt,
    "مقاله": article.prompt,
    "انشا": essay.prompt,
    "خلاصه سازی": summarizing.prompt,
    "سناریو ساخت ویدئو": video_production_scenario.prompt,
    "داستان": story.prompt,
    "داستان تخیلی": fiction_story.prompt,
}

tone_prompt = tone.prompt
words_number_prompt = words_length.prompt

prompts_titles: list[str] = [title for title in prompts]

tones = [
    "دوستانه",
    "کارشناس",
    "آموزنده",
    "قاطعانه",
    "احساسی",
    "رسمی",
    "حرفه ای",
    "خنثی",
    "با اعتماد بنفس",
    "طنز",
    "همدل",
    "متقاعد کننده",
]

words_number = [
    100,
    200,
    300,
    400,
    500,
]