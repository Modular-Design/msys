# The Plugin System

Plugins register automatically via python entrypoints. 
Types, Modules and complete Extensions have each there separate Entrypoint:

| Plugin-Type | Entrypoint          |
| ----------- | ------------------- |
| Type        | msys.types          |
| Module      | msys.modules        |
| Extensions  | msys.extensions     |
