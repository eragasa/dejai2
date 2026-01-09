filename: `dejai2.devbundle.00`
Date: 20060109
Status: draft
Purpose: define the minimum structure for a `dejai2` miniproject so ne work items are consistently scoped, testable, and promotable
##### links:
- [[dejai2.00]]
- 

# Process

## 1. Definition
#### Definition: `devbundle`
A `devbundle` is a self-contained, date-scoped unit of work with the structure and discipline of a small repository.

A `devbundle` is the smallest unit of work that is:
- scoped (explicit goal + non-goals)
	- A `devbundle` is expected to be carried out in a day.  
- implementable (clear procedure / API contract),
- testable (acceptance criteria),
- promotable (can be integrated into a larger pipeline),
- archivable (serves as a durable record of intent + decisions).

The work to be done in a `devbundle` is done by a `devnote`
- there exists a single schema for a `devnote`
- ideally the schema would be separable into two pieces for separation of concerns
	- `devnote.plan` - which specifies the work to be done (`overseer_agent`)
	- `devnote.report` - which specifies how the work is to be done (`working_agent`)
- practically, it might be difficult to scope out the `devnote.plan` requiring the `working_agent` to modify the `devnote.plan` to modify the scope/specification in order to fullfill the work task

## 2. Process
1. create `devnote.plan`
2. get `devbundle_id` which is unique
3. save `devnote.plan`
	1. name: `devnote.{devbundle_id}.plan`
	2. location: `{repo_root_dir}/dev/devnotes/
4. create `devbundle`
	- `devbundle_dir`
		- `{repo_root_dir}/dev/dev.{devbundle_id}`
	- make directories:
		- `{devbundle_dir}/`
		- `{devbundle_dir}/src/`
		- `{devbundle_dir}/tests/`
		- `{devbundle_dir}/examples/`
		- `{devbundle_dir}/history/`
		- `{devbundle_dir}/docs/`
		- `{devbundle_dir}/papers/`
	- copy template files:
		- `README.md`
			- src: `{devbundle_template_dir}/README.md
			- dst: `{devbundle_dir}/README.md`
		- `LICENSE`
			- src:`{devbundle_template_dir}/LICENSE`
			- dst:`{devbundle_dir}/LICENSE`
		- `{devbundle_dir}/pyproject.toml`
	- `git add {f} for f in files`
	- `git push`
5. copy `devnote.plan` to `devbundle`
	- `devbundle_dir={project_root_dir}/dev/{devbundle_dir}`
	- `devbundle_plan_name=devnote.{devbundle_id}.plan.md`
	- `devbundle_report_name=devnote.{devbundle_id}.report.md`
	- `dst`
		- `{dev_bundle_dir}/history/devnote.{dev_bundle_id}.plan`
		- `{dev_bundle_dir}/history/devnote.{dev_bundle_id}.report`
6. complete work
7. copy devnote_plan to (`{project_root_dir}/dev/devnotes/)
8. git add f in changes_files
9. git commit changes
10. git push

