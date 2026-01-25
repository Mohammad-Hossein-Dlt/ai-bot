# prompt0 = '''
# Step by step based on the outline you gave me in the previous message.
# About the مقدمه consisting of +200 words, 100% unique, optimized for SEO and written by humans in Farsi language with a title and 3 sub-headings that the topic presented in Covers the request.
# Cover.
# Instead of copying and pasting from other sources, write the article in your own language.
# Consider confusion and fragmentation when creating content, and ensure a high level of both without losing character or context.
# Use well-defined paragraphs that engage the reader. Write in a conversational style written by a human (use formal tone, use personal pronouns, keep it simple, engage the reader, use active voice, keep it brief, questions ask and use rhetoric and use similes and metaphors).
# Put * at the beginning and end of the title and all the titles of the article.
# Please only say about the مقدمه of the موضوع کاربر and do not use other titles.
# please do not ask me any question.
# Do not use the title of the article at the beginning of the text.
# Do not provide any footnotes in the text.
# Please just answer only in [Farsi] language. Please answer in [Persian] and [fluent]
# '''
#
# prompt1 = '''
# Step by step based on the outline you gave me in the previous message.
# About the بخش اول consisting of +200 words, 100% unique, optimized for SEO and written by humans in Farsi language with a title and 3 sub-headings (including headings H1) that the topic presented in Covers the request.
# Cover. Instead of copying and pasting from other sources, write the article in your own language.
# Consider confusion and fragmentation when creating content, and ensure a high level of both without losing character or context.
# Use well-defined paragraphs that engage the reader.
# Write in a conversational style written by a human (use formal tone, use personal pronouns, keep it simple, engage the reader, use active voice, keep it brief, questions ask and use rhetoric and use similes and metaphors).
# Put * at the beginning and end of the title and all the titles of the article.
# Please only say about the بخش اول of the موضوع کاربر and do not use other titles.
# please do not ask me any question.
# Do not use the title of the article at the beginning of the text.
# Do not provide any footnotes in the text.
# Please just answer only in [Farsi] language.
# Please answer in [Persian] and [fluent]
# '''
#
# prompt2 = '''
# Step by step based on the outline you gave me in the previous message.
# About the بخش دوم  consisting of +200 words, 100% unique, optimized for SEO and written by humans in Farsi language with a title and 3 sub-headings (including headings H1) that the topic presented in Covers the request.
# Cover.
# Instead of copying and pasting from other sources, write the article in your own language.
# Consider confusion and fragmentation when creating content, and ensure a high level of both without losing character or context.
# Use well-defined paragraphs that engage the reader.
# Write in a conversational style written by a human (use formal tone, use personal pronouns, keep it simple, engage the reader, use active voice, keep it brief, questions ask and use rhetoric and use similes and metaphors).
# Put * at the beginning and end of the title and all the titles of the article.
# Please only say about the بخش دوم  of the موضوع کاربر and do not use other titles.
# please do not ask me any question.
# Do not use the title of the article at the beginning of the text.
# Do not provide any footnotes in the text.
# Please just answer only in [Farsi] language.
# Please answer in [Persian] and [fluent]
# '''
#
# prompt3 = '''
# Step by step based on the outline you gave me in the previous message.
# About the بخش سوم consisting of +200 words, 100% unique, optimized for SEO and written by humans in Farsi language with a title and 3 sub-headings (including headings H1) that the topic presented in Covers the request.
# Cover.
# Instead of copying and pasting from other sources, write the article in your own language.
# Consider confusion and fragmentation when creating content, and ensure a high level of both without losing character or context.
# Use well-defined paragraphs that engage the reader.
# Write in a conversational style written by a human (use formal tone, use personal pronouns, keep it simple, engage the reader, use active voice, keep it brief, questions ask and use rhetoric and use similes and metaphors).
# Put * at the beginning and end of the title and all the titles of the article.
# Please only say about the بخش سوم of the موضوع کاربر and do not use other titles.
# please do not ask me any question.
# Do not use the title of the article at the beginning of the text.
# Do not provide any footnotes in the text.
# Please just answer only in [Farsi] language.
# Please answer in [Persian] and [fluent]
# '''
#
# prompt4 = '''
# Step by step based on the outline you gave me in the previous message.
# About the بخش چهارم  consisting of +200 words, 100% unique, optimized for SEO and written by humans in Farsi language with a title and 3 sub-headings (including headings H1) that the topic presented in Covers the request.
# Cover.
# Instead of copying and pasting from other sources, write the article in your own language.
# Consider confusion and fragmentation when creating content, and ensure a high level of both without losing character or context.
# Use well-defined paragraphs that engage the reader.
# Write in a conversational style written by a human (use formal tone, use personal pronouns, keep it simple, engage the reader, use active voice, keep it brief, questions ask and use rhetoric and use similes and metaphors).
# Put * at the beginning and end of the title and all the titles of the article.
# Please only say about the بخش چهارم  of the موضوع کاربر and do not use other titles.
# please do not ask me any question.
# Do not use the title of the article at the beginning of the text.
# Do not provide any footnotes in the text.
# Please just answer only in [Farsi] language.
# Please answer in [Persian] and [fluent]
# '''
#
# prompt5 = '''
# Step by step based on the outline you gave me in the previous message.
# About the نتیجه گیری  consisting of +200 words, 100% unique, optimized for SEO and written by humans in Farsi language with a title and 3 sub-headings (including headings H1) that the topic presented in Covers the request.
# Cover.
# Instead of copying and pasting from other sources, write the article in your own language.
# Consider confusion and fragmentation when creating content, and ensure a high level of both without losing character or context.
# Use well-defined paragraphs that engage the reader.
# Write in a conversational style written by a human (use formal tone, use personal pronouns, keep it simple, engage the reader, use active voice, keep it brief, questions ask and use rhetoric and use similes and metaphors).
# Put * at the beginning and end of the title and all the titles of the article.
# Please only say about the نتیجه گیری  of the موضوع کاربر and do not use other titles.
# please do not ask me any question.
# Do not use the title of the article at the beginning of the text. Do not provide any footnotes in the text.
# Please just answer only in [Farsi] language.
# Please answer in [Persian] and [fluent]
# '''
#
# ARTICLE_PROMPTS = [
#     prompt0,
#     prompt1,
#     prompt2,
#     prompt3,
#     prompt4,
#     prompt5,
# ]
#


prompt = '''

I want you to act as an expert content creator and generate a highly detailed, professional, and comprehensive 
article based on the topic I provide. The article should adhere to the following guidelines:

Form and Structure: Present the output in the form of a well-organized article. Start with an engaging introduction 
that sets the tone for the topic, followed by logically structured sections or headings that explore the subject 
matter in depth. Conclude with a thoughtful summary or call-to-action, depending on the context of the topic.

Role-Playing Expertise: Act as an expert in the topic I provide. Your response should reflect in-depth knowledge, 
expertise, and confidence on the subject matter.

Accuracy and Research: Provide accurate, well-researched, and comprehensive information. Include relevant facts, 
data, or insights that are up-to-date and aligned with industry standards or academic best practices.

Professionalism and Organization: Ensure the article is written in a polished, professional, and organized manner. 
Use proper grammar, punctuation, and language conventions. Include bullet points, numbered lists, or subheadings 
where necessary to enhance readability.

Neutrality and Flexibility: Present the information in a manner that avoids injecting personal opinions or biases 
unless explicitly required.

Neutrality and Impartiality: Maintain a neutral and unbiased tone throughout the email unless explicitly instructed 
otherwise.

Comprehensiveness and Finality: Provide the most complete and detailed response possible so that it addresses all 
potential aspects of the topic. The response should be so thorough that no further revisions or additional requests 
are necessary.

Language of Response: While the prompt and instructions are in English, the final article must be written in Farsi. 
Ensure that the Persian language used is fluent, professional, and culturally appropriate.

Please confirm that you understand these guidelines and proceed to craft the article based on the topic provided.

'''