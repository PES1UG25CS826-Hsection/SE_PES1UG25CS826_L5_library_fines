# Reflection

1. **Which issues were easiest and hardest to fix?**
   The formatting issues from Flake8 were easiest because they are mechanical. The hardest was replacing `eval()`, because I had to build a safe evaluator instead of just deleting a line.

2. **Did the tools report any false positives?**
   Not really. Pylint's docstring warnings were not bugs, but they improve maintainability, so I treated them as valid.

3. **How would you integrate static analysis into a workflow?**
   Run all three tools automatically on every commit or pull request (pre-commit hooks or CI), and block merges when Bandit finds medium or high severity issues.

4. **What improvements did you see in the code?**
   Pylint rose from 6.07 to X.XX, Bandit went from 2 findings to 0, and Flake8 from 14 to 0. The code is also safer and clearer, and some real bugs (shared default list, fine rate changing on renewal, negative fines) were fixed.
   