find . -name log.md -print0 | xargs -0 -I file cat file > merged_log.md
