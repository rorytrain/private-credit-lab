import os
from dotenv import load_dotenv
import anthropic
from datetime import datetime

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def load_portfolio_data(filepath):
    with open(filepath, "r") as f:
        return f.read()

def generate_lp_summary(portfolio_text):
    prompt = f"""You are a senior portfolio manager at a private credit alternatives platform.
You are preparing a quarterly LP update letter summarising the current state of the portfolio.

Your audience is a sophisticated institutional LP — a pension fund or family office.
They expect candour, precision and professional judgment. Do not obscure problems.
Do not use marketing language. Write in the register of a senior credit professional.

The summary should cover the following sections in order:
1. Portfolio Overview — one short paragraph summarising the portfolio at a glance
2. Active Positions — a brief update on each active deal, including covenant status
3. Pipeline — a brief note on deals under review and their current status
4. Declined Deals — one sentence confirming mandate discipline was applied
5. Risk Commentary — two to three sentences on the key risk in the portfolio
   and the platform's response

Formatting rules:
- Use plain prose, no bullet points
- Each section heading on its own line in capitals
- Maximum 450 words total
- Be direct about covenant breaches — do not soften them

PORTFOLIO DATA:
{portfolio_text}"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        temperature=0,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text

def main():
    print("Generating LP portfolio summary...\n")
    portfolio_text = load_portfolio_data("portfolio_data.txt")
    summary = generate_lp_summary(portfolio_text)

    print(summary)

    output_path = "lp_summary_q3_2026.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("LP QUARTERLY UPDATE\n")
        f.write("Silverstone Credit Partners LP\n")
        f.write("Period: Q3 2026\n")
        f.write("Generated: " + datetime.now().strftime("%Y-%m-%d %H:%M") + "\n")
        f.write("=" * 60 + "\n\n")
        f.write(summary)

    print("\nSummary written to " + output_path)

if __name__ == "__main__":
    main()
