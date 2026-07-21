from web_searching import web_search
from web_scraping import web_scrape

from llm_models import get_llm
from utilities import to_obj

from prompts import (
    ASSISTANT_SELECTION_PROMPT_TEMPLATE,
    WEB_SEARCH_PROMPT_TEMPLATE,
    SUMMARY_PROMPT_TEMPLATE,
    RESEARCH_REPORT_PROMPT_TEMPLATE,
)

# Setting constants and input variables
NUM_SEARCH_QUERIES = 2
NUM_SEARCH_RESULTS_PER_QUERY = 3
RESULT_TEXT_MAX_CHARACTERS = 10000

question = 'What can I see and do in the Spanish town of Astorga?'

# Instantianing the LLM client
llm = get_llm()

# Determine the correct research assistant and related instructions based on the user's research question
assistant_selection_prompt = ASSISTANT_SELECTION_PROMPT_TEMPLATE.format(user_question=question)
assistant_instructions = llm.invoke(assistant_selection_prompt)
print(assistant_instructions)

assistant_instructions_dict = to_obj(assistant_instructions.content)    # To convert it into a Python object
print(assistant_instructions_dict)

# Generate web searches based on the original user research question
web_search_prompt = WEB_SEARCH_PROMPT_TEMPLATE.format(
    assistant_instructions=assistant_instructions_dict['assistant_instructions'],
    num_search_queries=NUM_SEARCH_QUERIES,
    user_question=assistant_instructions_dict['user_question']
)
web_search_queries = llm.invoke(web_search_prompt)
web_search_queries_list = to_obj(web_search_queries.content.replace('\n', ''))

# Fetch web searches using web_search() function
search_and_result_urls = [{
    'result_urls': web_search(
        web_query=wq['search_query'],
        num_results=NUM_SEARCH_RESULTS_PER_QUERY),
    'search_query': wq['search_query']}
for wq in web_search_queries_list]

print("=============== SEARCH QUERY ===============")
print(search_and_result_urls)

# Flatten the results so each dictionary contains a search query and just one result URL
search_query_and_result_url_list = []
for qr in search_and_result_urls:
    search_query_and_result_url_list.extend([
        {
            'search_query': qr['search_query'],
            'result_url': r
        }
        for r in qr['result_urls']
    ])

print("=============== RESULT URL ===============")
print(search_query_and_result_url_list)

# Use the web_scrape() function to pull text from web pages linked through your search results.
result_text_list = [
    {
        'result_text': web_scrape(url=re['result_url'])[:RESULT_TEXT_MAX_CHARACTERS],
        'result_url': re['result_url'],
        'search_query': re['search_query']
    }
    for re in search_query_and_result_url_list
]

print("=============== WEB SCRAPE ===============")
print(result_text_list)

# Ask the LLM to summarize the text from each web page and also keep the original search queries and URLs.
result_text_summary_list = []
for rt in result_text_list:
    summary_prompt = SUMMARY_PROMPT_TEMPLATE.format(
        search_result_text=rt['result_text'],
        search_query=rt['search_query']
    )

    text_summary = llm.invoke(summary_prompt)

    result_text_summary_list.append({
        'text_summary': text_summary,
        'result_url': rt['result_url'],
        'search_query': rt['search_query']
    })

print("=============== SUMMARY ===============")
print(result_text_summary_list)

# Generate the final report
stringified_summary_list = [
    f"Source URL: {sr['result_url']}\nSummary: {sr['text_summary']}"
    for sr in result_text_summary_list
]

print("=============== STRINGIFIED SUMMARY ===============")
print(stringified_summary_list)

# Combine all the summary strings into one
appended_result_summaries = '\n'.join(stringified_summary_list) # A single text block with all summaries and URLs

# Get the final research report
research_report_prompt = RESEARCH_REPORT_PROMPT_TEMPLATE.format(
    research_summary=appended_result_summaries,
    user_question=question
)
research_report = llm.invoke(research_report_prompt)

print("=============== FINAL RESEARCH REPORT ===============")
print(f'strigified_summary_list={stringified_summary_list}')
print(f'merged_result_summaries={appended_result_summaries}')
print(f'research_report={research_report}')