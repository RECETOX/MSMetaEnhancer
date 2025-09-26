# Contributing

We welcome any kind of contribution to our software, from simple comment or question to a full fledged [pull request](https://help.github.com/articles/about-pull-requests/).

A contribution can be one of the following cases:

1. you have a question;
1. you think you may have found a bug (including unexpected behavior);
1. you want to make some kind of change to the code base (e.g. to fix a bug, to add a new feature, to update documentation);

The sections below outline the steps in each case.

## You have a question

1. use the search functionality in the issues to see if someone already filed the same issue;
1. if your issue search did not yield any relevant results, make a new issue;

## You think you may have found a bug

1. use the search functionality in the issues to see if someone already filed the same issue;
1. if your issue search did not yield any relevant results, make a new issue, making sure to provide enough information to the rest of the community to understand the cause and context of the problem. Depending on the issue, you may want to include:
    - some identifying information (name and version number) for dependencies you're using;
    - information about the operating system;

## You want to make some kind of change to the code base

In case you feel like you've made a valuable contribution, but you don't know how to write or run tests for it, or how to generate the documentation: don't let this discourage you from making the pull request; we can help you! Just go ahead and submit the pull request, but keep in mind that you might be asked to append additional commits to your pull request.

1. (**important**) announce your plan to the rest of the community *before you start working*. This announcement should be in the form of a (new) issue;
1. (**important**) wait until some kind of consensus is reached about your idea being a good idea;
1. if needed, fork the repository to your own Github profile and create your own feature branch off of the latest master commit. While working on your feature branch, make sure to stay up to date with the main branch by pulling in changes, possibly from the 'upstream' repository (follow the instructions [here](https://help.github.com/articles/configuring-a-remote-for-a-fork/) and [here](https://help.github.com/articles/syncing-a-fork/));
1. make sure the existing tests still work by running ``pytest``;
1. add your own tests (if necessary);
1. update or expand the documentation;
1. update the [CHANGELOG](CHANGELOG.md) file with change;
1. [push](http://rogerdudler.github.io/git-guide/>) your feature branch to (your fork of) this repository on GitHub;
1. create the pull request, e.g. following the instructions [here](https://help.github.com/articles/creating-a-pull-request/).

## Adding a new service to MSMetaEnhancer

MSMetaEnhancer has a modular architecture that makes it easy to add new conversion services. There are two main types of converters:

- **Web Converters**: Services that make HTTP requests to external APIs
- **Compute Converters**: Services that perform local computations

### Architecture Overview

The MSMetaEnhancer system consists of several key components:

1. **Base Converter Classes**:
   - `Converter`: Abstract base class for all converters
   - `WebConverter`: Base class for web-based API services
   - `ComputeConverter`: Base class for local computation services

2. **Job System**: 
   - `Job`: Represents a conversion task (source → target using specific converter)
   - Jobs are defined as tuples: `(source_attribute, target_attribute, converter_name)`

3. **Converter Builder**: 
   - Automatically discovers and instantiates available converters
   - Manages both web and compute converters

4. **Dynamic Method Creation**: 
   - Converters automatically generate methods like `compound_name_to_inchi()`
   - Based on the conversions list defined in each converter

### Adding a new Web Converter

To add a new web-based service, follow these steps:

#### 1. Create the converter file

Create a new Python file in `MSMetaEnhancer/libs/converters/web/` named after your service (e.g., `MyService.py`).

#### 2. Implement the converter class

```python
from MSMetaEnhancer.libs.converters.web.WebConverter import WebConverter

class MyService(WebConverter):
    """
    Brief description of what your service does.
    
    Service URL: https://example.com/api
    """
    
    def __init__(self, session):
        super().__init__(session)
        
        # Define the service endpoints
        self.endpoints = {
            'MyService': 'https://api.example.com/v1/'
        }
        
        # Define the conversions this service supports
        conversions = [
            ('source_attr', 'target_attr', 'conversion_method'),
            # Add more conversions as needed
        ]
        self.create_top_level_conversion_methods(conversions)
        
        # Add rate limiting if needed (optional)
        # self.throttler = Throttler(rate_limit=5)  # 5 requests per second
        
    async def conversion_method(self, input_data):
        """
        Implement the actual conversion logic.
        
        :param input_data: The input data to convert
        :return: Dictionary with converted data
        """
        # Build the API request
        args = f'endpoint/{input_data}'
        
        # Make the request (with throttling if configured)
        response = await self.query_the_service('MyService', args)
        
        # Parse and return the result
        if response:
            return self.parse_response(response)
        return {}
        
    def parse_response(self, response):
        """
        Parse the API response and extract relevant data.
        
        :param response: Raw API response
        :return: Dictionary with parsed data
        """
        # Implement response parsing logic
        # Return a dictionary with attribute names as keys
        return {'target_attr': parsed_value}
```

#### 3. Register the converter

Add your new converter to `MSMetaEnhancer/libs/converters/web/__init__.py`:

```python
from MSMetaEnhancer.libs.converters.web.MyService import MyService

__all__ = ['IDSM', 'CTS', 'CIR', 'PubChem', 'BridgeDb', 'MyService']
```

#### 4. Add tests

Create a test file `tests/test_MyService.py`:

```python
import pytest
from MSMetaEnhancer.libs.converters.web.MyService import MyService

@pytest.mark.dependency()
async def test_service_available():
    """Test if the service is available."""
    # Implementation depends on your service
    pass

@pytest.mark.dependency(depends=["test_service_available"])
async def test_conversion():
    """Test the conversion functionality."""
    # Mock the service and test your conversion methods
    pass
```

### Adding a new Compute Converter

For local computation services (like RDKit), follow these steps:

#### 1. Create the converter file

Create a new Python file in `MSMetaEnhancer/libs/converters/compute/` named after your service.

#### 2. Implement the converter class

```python
from MSMetaEnhancer.libs.converters.compute.ComputeConverter import ComputeConverter

class MyComputeService(ComputeConverter):
    """
    Description of your compute service.
    """
    
    def __init__(self):
        super().__init__()
        
        # Define the conversions this service supports
        conversions = [
            ('source_attr', 'target_attr', 'conversion_method'),
            # Add more conversions as needed
        ]
        self.create_top_level_conversion_methods(conversions, asynch=False)
        
    def conversion_method(self, input_data):
        """
        Implement the computation logic.
        
        :param input_data: The input data to process
        :return: Dictionary with computed data
        """
        # Perform local computation
        result = some_computation(input_data)
        return {'target_attr': result}
```

#### 3. Register the converter

Add your new converter to `MSMetaEnhancer/libs/converters/compute/__init__.py`:

```python
from MSMetaEnhancer.libs.converters.compute.MyComputeService import MyComputeService

__all__ = ['RDKit', 'MyComputeService']
```

### Adding conversion functions to existing services

To add new conversion functions to existing converters:

#### 1. Add the conversion method

Add a new method to the existing converter class:

```python
async def new_conversion_method(self, input_data):
    """
    Description of what this conversion does.
    
    :param input_data: Input data
    :return: Converted data
    """
    # Implementation here
    pass
```

#### 2. Register the conversion

Add the new conversion to the `conversions` list in the `__init__` method:

```python
conversions = [
    # existing conversions...
    ('new_source_attr', 'new_target_attr', 'new_conversion_method'),
]
```

### Key principles for converter development

1. **Error Handling**: Always handle API errors gracefully and return empty dictionaries when data is not available
2. **Rate Limiting**: Respect API rate limits using throttling mechanisms
3. **Data Validation**: Validate input data before making API calls
4. **Response Parsing**: Implement robust response parsing that handles various response formats
5. **Documentation**: Include docstrings for all methods explaining parameters and return values
6. **Testing**: Write comprehensive tests including service availability and conversion functionality

### Testing your changes

After implementing your converter:

1. Run the existing tests to ensure you haven't broken anything:
   ```bash
   pytest tests/
   ```

2. Run your specific tests:
   ```bash
   pytest tests/test_YourService.py -v
   ```

3. Test the integration by using the converter in a real scenario

### Common patterns and utilities

- **Throttling**: Use `Throttler` class for rate limiting
- **Caching**: Use `@lru_cache` decorator for caching responses
- **Error handling**: Inherit from base converter classes for consistent error handling
- **Data escaping**: Use decorators like `@escape_single_quotes` for input sanitization

### Template files

To help you get started quickly, you can use these template files as starting points:

- **Web Converter Template**: Use the CTS or PubChem converters as reference implementations
- **Compute Converter Template**: Use the RDKit converter as a reference implementation
- **Test Template**: Follow the existing test patterns in the `tests/` directory

These templates include:
- Proper class structure and inheritance
- Common import patterns
- Standard method signatures
- Error handling patterns
- Documentation structure
- Test structure and mocking examples
