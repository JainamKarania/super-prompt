# Separate instructions from data with delimiters
Source: https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview

When a prompt mixes instructions with material to work on, such as an email to summarize or code to review, separate them with clear markers. Use tags like <document>...</document>, triple quotes, or headings. This stops the model from confusing the material with the instructions, and it makes the prompt easier to read and reuse. It also reduces the risk that text inside the material is treated as a command.
