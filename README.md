# Empório da Música – Virtual Assistant

A customer service agent for a (fictional) musical instrument store, built in Python
with Google Gemini. The customer chats in the terminal, in Brazilian Portuguese, and the
agent answers about products, prices, stock, installments, orders and store policies.

The agent uses **function calling**: the language model decides *when* to look something
up, and my code does the lookup and the calculations. The model only writes the final answer.

## About this project

This is my first Python project and my first time working with an LLM API. My background is
TypeScript, JavaScript, React and Node, so I built this case as a way to learn by doing,
under a tight deadline. I tried to make decisions I can explain, to keep the code simple, and
to be honest about what is missing (see *Known limitations*). My English is intermediate: I
used a translator and an AI assistant to write the English text in this README, in the system
prompt and in the tool docstrings.

## How to run

Requirements: Python 3.12 and a Gemini API key (free tier from Google AI Studio is enough).

```bash
git clone https://github.com/danielalves5612/emporio-agent.git
cd emporio-agent
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # then open .env and paste your key
python main.py
```

Type your message after the `>` prompt. Type `sair` to leave.

Notes:
- The model name is set in `src/agent.py` (`MODEL_NAME`). It was `gemini-3.5-flash` when I
  built the project. Model names change often, so you may need to update it.
- The free tier has a daily request limit. If you reach it, the chat shows a short
  "system unstable" message and stays open.

## Project structure

```
main.py                 chat loop in the terminal
src/agent.py            system prompt, Gemini chat session, tool registration
src/tools.py            the 4 tools the model can call
src/product_search.py   search by name and availability rule
src/order_lookup.py     order lookup and email verification
src/payments.py         PIX price and installment rules
src/data_loader.py      loads the CSV files and the policy PDF
data/                   CSV tables and the policy manual (PDF) from the case
examples/               5 example conversations (see below)
```

## What the agent can do

| Tool | What it does |
|---|---|
| `find_products` | Finds products by part of the name. Returns price, stock and an availability label (`available`, `out_of_stock`, `discontinued`, `coming_soon`). |
| `browse_products` | Lists products that can be bought now in a category, up to a price, cheapest first. |
| `calculate_payment_options` | Returns the PIX price, the maximum number of installments and the installment value. |
| `get_order_status` | Returns the status of an order, only if the email matches the customer who made it. |

Store information (address, opening hours, returns, shipping, warranty) is answered from the
policy manual, which is loaded into the system prompt. Questions outside the store's scope
(for example accessories, which the store does not sell, or unrelated topics) are declined politely.

## Technical decisions

**Function calling instead of RAG.** The policy manual is short (8 pages, about 14,000
characters), so it fits in the model's context. I read the PDF once at startup and append it
to the system prompt. This is simpler and more reliable than a vector database for a document
this size. For a larger knowledge base I would use retrieval.

**Business rules live in code, not in the prompt.** A prompt is an instruction, not a
guarantee. The rules that must not fail are plain Python functions:
- availability = status + stock (`get_availability`);
- installments and PIX price (`src/payments.py`);
- order privacy (`verify_order_owner`).

The model only repeats what the tools return. During tests the model once promised
"12x without interest" for products that cannot be split that much, and later a wrong
installment value came from my own bug. Both cases were easy to fix because the calculation
is in one place.

**Privacy of orders.** The order tool needs the order number and the customer's email.
If the order does not exist or the email does not match, the tool returns the same error in
both cases, so nobody can discover which order numbers exist. It returns only four fields
(`order_id`, `status`, `order_date`, `estimated_delivery`), never the whole record. The email
comparison ignores case and extra spaces.

**Tools return simple data.** Tools return lists and dictionaries instead of pandas tables,
because the model can only read simple JSON-like data. The tool docstrings are written for the
model: they say when to use the tool and what it returns.

**Conversation history.** The terminal uses a Gemini chat session, so the agent remembers the
previous messages (for example "and is it in stock?" after a price question). The history lives
only in memory and is lost when the program closes.

**Errors.** If the API fails (overloaded server or quota reached), the chat shows a message in
Portuguese and keeps running instead of crashing.

**Choice of model.** I tested models with the question "Quanto custa o Yamaha C40?" before the
data tools were connected, with a system prompt that forbids inventing prices. The real price
is R$ 599.90. Each test was a single run, and times varied a lot with server load.

| Model | Time | Invented a price? |
|---|---|---|
| `gemini-flash-lite-latest` | 2.6 s | **Yes** (R$ 899.00 and "10x without interest") |
| `gemini-flash-latest` | 1 min 12 s | No |
| `gemini-3.8-flash` | 31.5 s (other runs: 1 min 42 s, 2 min 29 s) | No |
| `gemini-3.5-flash` | much faster in the chat | No (see examples) |

The small model was fast but ignored the instruction. I kept `gemini-3.5-flash` because it
followed the rules and answered quickly. `gemini-2.5-flash` returned a 404 for my account.

## Assumptions about the policy manual

The manual has a few inconsistencies. This is what I assumed, and the store should confirm it:
- **Phone numbers:** the manual lists (67) 3341-4444 (company data) and (67) 3321-4500
  (WhatsApp channel). The agent gives each number for its channel.
- **Email:** it appears with and without an accent. I used `contato@emporiodamusica.com.br`.
- **Installments:** section 3.1 gives minimum installment values by number of installments
  (R$ 50 up to 3x, R$ 80 from 4x to 6x, R$ 100 from 7x to 12x). The payment table says R$ 100
  for any installment plan. I followed section 3.1, the detailed rule.
- **Internal document:** the manual says it is for internal use, so the agent is instructed
  not to mention it and to answer in its own words.

## Example conversations

The `examples/` folder has real conversations with the final version of the agent:

1. `01-catalog-and-pix.md`: category and price search, then PIX and installments.
2. `02-store-info-and-returns.md`: address, opening hours and the return policy.
3. `03-orders-and-scope.md`: order status with email check, a wrong email, and an out-of-scope request.
4. `04-product-price.md`: price lookup with payment conditions.
5. `05-out-of-stock.md`: a product with no stock and suggestions of similar products.

## Known limitations

- **Promotions are not implemented.** The manual says promotional prices do not combine with
  the PIX discount, and the promotions table exists, but the agent does not read it. During a
  promotion, the PIX price could be wrong.
- The order tool does not return the products of an order, and `estimated_delivery` is a
  forecast date, so the agent may describe it as if it were the delivery date.
- The free tier has a daily request limit and the servers were sometimes overloaded. Answers
  took from a few seconds to a few minutes.
- The whole manual goes into every request. This is fine for 14,000 characters but does not scale.
- The conversation history is not saved to disk.
- There are no automated tests yet. I tested the functions by hand and checked the agent's
  answers against the data tables.
- There is no hand-off to a human attendant. The agent only offers to pass the question on.
- My Python is still basic. The code is simple on purpose, and I know it can be improved
  (type hints, tests, better structure).

## What I would do with more time

- Add a promotions tool and apply the "no PIX discount on promotional prices" rule in code.
- Add `pytest` tests for availability, installments, PIX price and order verification, and a
  small set of questions to check the agent's answers automatically.
- Stream the answer while it is generated, so the customer does not wait for the full text.
- Add a simple web interface (I usually work with React and Node), keeping the Python agent
  as an API.
- Save the conversation history, and use retrieval if the knowledge base grows.
- Keep studying Python itself: the standard library, pandas, testing and good practices.

## How I used AI assistants

I had never written Python or used an LLM API before this project. Instead of asking an
assistant to generate the whole project, I chose to learn by building it step by step,
because I wanted to understand what I was delivering and to be able to discuss it.

- **Claude (chat), as tutor and reviewer:** I asked for each concept to be explained with
  JavaScript comparisons (pandas filters, function calling, system prompts). Claude gave me
  guided exercises, usually a code skeleton with blanks to complete, and some larger blocks
  for me to review and adapt (for example the catalog and payment tools). I typed and ran
  the code, brought back the outputs and the errors, and asked why they happened.
  Claude also drafted the English system prompt and the tool docstrings, and helped with
  my English.
- **What I decided and checked myself:** the workflow (one branch per feature, pull
  requests, conventional commit messages, Ruff for formatting), the comparison of three
  models and the final model choice. I checked the agent's answers against the data
  tables. That is how we found an invented price and, later, a wrong installment value
  caused by a bug in my code.
- **Gemini:** the language model inside the agent.
- **Translator:** for English words I did not know.

I am happy to walk through any file and decision, and I know I still have a lot to learn
about Python. The commit history shows how the project was built, step by step.