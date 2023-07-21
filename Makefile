#
# deps
#
.PHONY: deps-sync # sync dependencies
deps-sync:
	poetry install --sync

.PHONY: deps-show # build source and wheel
deps-show:
	poetry show

#
# publishing
#
.PHONY: package-publish # publish to pypi
package-publish:
	poetry publish

.PHONY: package-publish-test # publish to test.pypi
package-publish-test:
	poetry publish -r test-pypi

.PHONY: package-build # build source and wheel
package-build:
	poetry build

.PHONY: package-version-bump-patch # bump patch version
package-version-bump-patch:
	poetry version patch

.PHONY: package-version-bump-prerelease # bump prerelease version
package-version-bump-prerelease:
	poetry version prerelease

#
# tests
#
.PHONY: spin # run all checks
spin: typecheck lint test-quiet

.PHONY: test # run test
test:
	pytest

# mypy won't report anything if you haven't type hinted/annotated your code
.PHONY: typecheck # run mypy
typecheck:
	mypy .

.PHONY: lint # run linter
lint:
	#ruff .
	isort . --check-only
	black . --check

.PHONY: test-quiet # run test quietly
test-quiet:
	pytest -q

.PHONY: test-dry-run # dry-run test, just get test names
test-dry-run:
	pytest --collect-only

include Makefile.common
