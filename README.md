# mapped-enum

[![PyPI version](https://badge.fury.io/py/mapped-enum.svg)](https://badge.fury.io/py/mapped-enum)

`Enum`s that can easily map to and from arbitrary values of another type.

## Summary

There are many cases in Python where you want to asscociate an `Enum` class with more meaningful values than
the default integers from `auto()`. Python allows assignment of anything as a value of an enum member, but there is still no indication of what that value represents.
When accessing tuple values, one can only refer to each tuple member by its index, creating further ambiguity.

`mapped-enum` seeks to solve that problem by dynamically populating the enum keys with custom value names. For example,
you can have a `DaysOfWeek` enum with fields `index`, `short_name`, and `full_name`. When that enum is mapped using this module, 
accessing those values becomes as simple as:

```
>>> DaysOfWeek.MONDAY.to_short_name()
'mon'
>>> DaysOfWeek.TUESDAY.to_index()
1
>>> DaysOfWeek.FRIDAY.to_full_name()
'Friday'
```

Mapping in the other direction is just as easy:

```
>>> DaysOfWeek.from_short_name('mon')
<DaysOfWeek.MONDAY: (0, 'mon', 'Monday')>
```

## Usage

This module provides the `enum_map` function, which is to be used as an annotation on a class inherting from 
`Enum`. The annotation takes one required argument `keys`, an array of strings representing the names of the fields to
generate.  The value of each enum member should be a tuple, with the data arranged such that each tuple member corresponds
to a string name from the annotation argument.

For each key specified in the `keys` parameter, a method called `to_<key>` and a class method called
`from_<key>` will be added to the enum. These convert to and from the enum values at the index of the keyword.

### Generated methods

`to_<key>` is called on an enum member and takes no arguments. It returns the indexed member of the enum value tuple
corresponding to the index of the `key`word.

`from_<key>` is called directly on the enum class. It takes a single argument, the value to search for enum members
with the value index corresponding to the index of the `key`word. If there is no enum member that satisfies the
requested value, it will return `None`.

### Optional arguments

The annotation can take a number of optional arguments to modify its behavior.

| Parameter name | Type | Purpose |
| - | - |
| `to_prefix` | `str` | An alternative prefix for the conversion methods instead of `to_`. |
| `from_prefix` | An alternative prefix for the lookup methods instead of `from_`. |
| `allow_override` | If True, if the enum defines methods with the same name as a possible `enum_map` method, the `enum_map` method will be silently overridden. Otherwise, an error will be thrown. |
| `multiple_from` | If True, calls to a `from_` method with multiple members matching the search term will return all of those members; consequently, such a call with no matching members will return an empty list. If False, then calls to a `from_`  method will return the first matching term, or None if no match is found. |
