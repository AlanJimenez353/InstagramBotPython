import openai

def get_fun_facts(api_key, n=10):
    openai.api_key = api_key
    prompt = "Dame 10 datos curiosos"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    facts = response.choices[0].text.strip().split('\n')
    return facts[:n]
