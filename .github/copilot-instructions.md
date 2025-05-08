## Guidelines for Creating or Updating a Plan

- When creating a plan, organize it into numbered phases (e.g., "Phase 1: Setup Dependencies")
- Break down each phase into specific tasks with numeric identifiers (e.g., "Task 1.1: Add Dependencies")
- Please only create one document per plan
- Mark phases and tasks as `- [ ]` while not complete and `- [x]` once completed
- End the plan with success criteria that define when the implementation is complete
- Plans that you produce should go under `docs/plans`
- Use a consistent naming convention `YYYYMMDD-<short-description>.md` for plan files

## Guidelines for Implementing a Plan

- Always prefer the latest Python 3.11 syntax and language features. Avoid deprecated patterns and legacy syntax, especially in type annotations and built-in generics.
- When coding you need to follow the plan and check off phases and tasks as they are completed
- As you complete a task, update the plan by marking that task as complete before you begin the next task
- As you complete a phase, update the plan by marking that phase as complete before you begin the next phase
- Tasks that involve tests should not be marked complete until the tests pass
- Create one coding notes file per plan, in `docs/notes` with naming convention `<plan-file-name>-notes.md`
  - Include a link to the plan file
- When you complete implementation for a plan phase, create a notes entry in the notes file for the plan and summarize the completed work as follows:

```markdown
## Phase <phase-number>: <phase-name>
- Completed on: <current UTC date and time>
- Completed by: <name of the person who completed the phase, not Copilot>

### Major files added, updated, removed
<list of files and brief summary of changes>

### Major features added, updated, removed
<list of features and brief summary of changes>

### Patterns, abstractions, data structures, algorithms, etc.
<list of patterns, abstractions, data structures, algorithms, etc. and brief summary of changes>

### Governing design principles
<list of design principles and brief summary of changes>
```

## Python Coding Guidelines

### Use `|` instead of `Union`

Use the newer syntax of `a | b` instead of `Union[a, b]`.

### Prefer union with `None` over `Optional`

Use the newer syntax of `a | None` instead of `Optional[a]`.

### Don't use deprecated aliases

For type hints, use newer aliases like `list`, `dict` and `tuple` instead of
deprecated ones like `List`, `Dict` and `Tuple`. The full list is below:

<!--
This comment contains the instructions for generating the list below.

Run, assuming `uv` is installed:

    curl https://docs.python.org/3/library/typing.html |
        uvx markitdown@0.1.1 > typing.md

Give the remaining text of this comment as the prompt to Copilot:

Read `typing.md` and write a very brief bullet list of deprecated aliases, e.g.:

- Use `list[T]` instead of `List[T]`
-->

- Use `list[T]` instead of `List[T]`
- Use `dict[KT, VT]` instead of `Dict[KT, VT]`
- Use `list[T]` instead of `List[T]`
- Use `set[T]` instead of `Set[T]`
- Use `frozenset[T]` instead of `FrozenSet[T]`
- Use `tuple[T, ...]` instead of `Tuple[T, ...]`
- Use `type[C]` instead of `Type[C]`
- Use `collections.defaultdict[KT, VT]` instead of `DefaultDict[KT, VT]`
- Use `collections.OrderedDict[KT, VT]` instead of `OrderedDict[KT, VT]`
- Use `collections.ChainMap[KT, VT]` instead of `ChainMap[KT, VT]`
- Use `collections.Counter[T]` instead of `Counter[T]`
- Use `collections.deque[T]` instead of `Deque[T]`
- Use `re.Pattern[AnyStr]` instead of `Pattern[AnyStr]`
- Use `re.Match[AnyStr]` instead of `Match[AnyStr]`
- Use `str` instead of `Text`
- Use `collections.abc.Set[T]` instead of `AbstractSet[T]`
- Use `collections.abc.Collection[T]` instead of `Collection[T]`
- Use `collections.abc.Container[T]` instead of `Container[T]`
- Use `collections.abc.ItemsView[KT, VT]` instead of `ItemsView[KT, VT]`
- Use `collections.abc.KeysView[KT]` instead of `KeysView[KT]`
- Use `collections.abc.Mapping[KT, VT]` instead of `Mapping[KT, VT]`
- Use `collections.abc.MappingView` instead of `MappingView`
- Use `collections.abc.MutableMapping[KT, VT]` instead of `MutableMapping[KT, VT]`
- Use `collections.abc.MutableSequence[T]` instead of `MutableSequence[T]`
- Use `collections.abc.MutableSet[T]` instead of `MutableSet[T]`
- Use `collections.abc.Sequence[T]` instead of `Sequence[T]`
- Use `collections.abc.ValuesView[VT]` instead of `ValuesView[VT]`
- Use `collections.abc.Coroutine[YieldType, SendType, ReturnType]` instead of `Coroutine[YieldType, SendType, ReturnType]`
- Use `collections.abc.AsyncGenerator[YieldType, SendType]` instead of `AsyncGenerator[YieldType, SendType]`
- Use `collections.abc.AsyncIterable[T]` instead of `AsyncIterable[T]`
- Use `collections.abc.AsyncIterator[T]` instead of `AsyncIterator[T]`
- Use `collections.abc.Awaitable[T]` instead of `Awaitable[T]`
- Use `collections.abc.Iterable[T]` instead of `Iterable[T]`
- Use `collections.abc.Iterator[T]` instead of `Iterator[T]`
- Use `collections.abc.Callable[Params, ReturnType]` instead of `Callable[Params, ReturnType]`
- Use `collections.abc.Generator[YieldType, SendType, ReturnType]` instead of `Generator[YieldType, SendType, ReturnType]`
- Use `collections.abc.Hashable` instead of `Hashable`
- Use `collections.abc.Reversible[T]` instead of `Reversible[T]`
- Use `collections.abc.Sized` instead of `Sized`
- Use `contextlib.AbstractContextManager[T_co, ExitT_co]` instead of `ContextManager[T_co, ExitT_co]`
- Use `contextlib.AbstractAsyncContextManager[T_co, AExitT_co]` instead of `AsyncContextManager[T_co, AExitT_co]`

### Prefer `object` over `Any`

Prefer to use `object` instead of `Any`, and `cast` or `assert` as necessary.

For example, suppose the following dictionary:

```python
data: dict[str, object] = {
    "foo": 1,
    "bar": [2, 3, 4],
    "baz": True,
}
```

When the actual type can be assumed, use `cast`:

```python
from typing import cast

foo = cast(int, data["foo"])
bar = cast(list[int], data["bar"])
baz = cast(bool, data["baz"])
```

When checking the type at run-time via `isinstance`, the type checker like
Pyright may issue a `reportUnknownArgumentType` error for generic types on
usage since the type arguments may still be unknown, e.g.:

```python
bar = data["bar"] # here "bar" is "object"
if isinstance(bar, list): # "bar" is now narrowed to "list", but...
    print(bar) # ...argument type is "list[Unknown]" (reportUnknownArgumentType)
```

Use `cast` if the type argument can be assumed, like so:

```python
if isinstance(bar, list): # "bar" is now narrowed to "list[Unknown]"
    bar = cast(list[int], bar) # "bar" is narrowed to "list[int]"
    for item in bar:
        print(item * 2)
```

An alternative would be to assume `object` for the type argument and then
`assert` before using the contained values, as in:

```python
if isinstance(bar, list):
    bar = cast(list[object], bar)
    for item in bar:
        assert isinstance(item, int)
        print(item * 2)
```