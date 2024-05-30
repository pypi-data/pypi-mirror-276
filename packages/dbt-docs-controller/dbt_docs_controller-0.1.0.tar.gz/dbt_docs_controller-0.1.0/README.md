# dbt-docs-controller📑💾🕹️

`dbt-docs-controller` is a Python CLI tool designed to generate a documentation site for a subset of models in your dbt (data build tool) project.

## 📝Description:

In standard dbt-docs, documentation is generated for the entirety of your dbt project, including:
- All models
- All sources
- All macros

This approach might be overwhelming for end-users who are only interested in a specific part of your project. `dbt-docs-controller` addresses this by allowing you to generate documentation for only the relevant models and components that your end-users will actually interact with. This CLI empowers users to selectively include only the models, sources, packages, or combinations thereof that are relevant to their needs. Whether users require documentation for a single model, a group of sources, specific packages, or custom combinations, dbt-docs-controller makes the process effortless and efficient.

### 🔑✨Key Features:
- **Selective Documentation**: Generate documentation for specific models, sources, packages, or custom combinations thereof.
- **Simplified Output**: Create a cleaner, more focused dbt-docs site by excluding unnecessary nodes.
- **Easy to Use**: Simple CLI interface for quick integration into your existing dbt workflow.

### ⚙️💡How It Works:
`dbt-docs-controller` works by editing the `manifest.json` file used by the dbt-docs site. By selectively modifying the file based on user input, the tool ensures that only the specified components are included in the final documentation site, resulting in a documentation site that is precisely tailored to meet your specific needs and preferences.
