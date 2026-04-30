---
name: controller-api-doc-generator
description: Generates API documentation from Spring Boot Controller classes. Invoke when user needs to create API docs for Controller endpoints, including DTO properties and response examples.
---

# Controller API Documentation Generator

This skill generates comprehensive API documentation from Spring Boot Controller classes, including endpoint details, request parameters, response formats, and DTO property documentation.

## When to Use
Invoke this skill when:
- You need to generate API documentation for Spring Boot Controller endpoints
- User requests documentation with detailed DTO properties
- Documentation needs to include request/response examples
- User wants standardized API documentation format

## Prerequisites
- Spring Boot project with Controller classes
- Java DTO classes with validation annotations
- Lombok annotations (optional but supported)

## Generation Steps

### Step 1: Identify Target Controller
1. Locate the Controller class (e.g., `ShipApplyController.java`)
2. Analyze the Controller's endpoints, request methods, and parameters
3. Identify all DTO classes used in the Controller

### Step 2: Extract Controller Information
1. Read the Controller file to get:
   - Request mapping URL (class-level and method-level)
   - HTTP methods (GET, POST, PUT, DELETE, etc.)
   - Endpoint descriptions (from comments)
   - Request parameters (path variables, query parameters, request bodies)
   - Response types

### Step 3: Analyze DTO Structures
1. Identify all DTO classes referenced in the Controller
2. Read each DTO file to extract:
   - Field names and types
   - Validation annotations (@NotNull, @Size, @NotBlank, etc.)
   - Comment descriptions
   - Nested DTOs and List<> generics
   - Required status and length constraints

### Step 4: Generate Documentation
1. **API Endpoint Documentation**:
   - URL and HTTP method
   - Endpoint description
   - Request parameters (path, query, body)
   - Response structure and examples
   - Error codes and messages

2. **DTO Property Documentation**:
   - DTO hierarchy diagram
   - Detailed property tables for each DTO
   - Field name, Chinese description, data type
   - Required status and length constraints
   - Validation rules and default values

3. **Format Options**:
   - Markdown (MD)
   - HTML (for better readability)

## Example Usage

### Input
```java
@RestController
@RequestMapping("/shipApply")
public class ShipApplyController {
    
    @PostMapping("/tempStorage")
    public Response tempStorage(@RequestBody ShipApplyDTO dto) {
        return vesselShipInfoService.tempStorage(dto);
    }
}
```

### Output Structure
```markdown
# ShipApplyController API Documentation

## 1. 接口列表

### 1.1 暂存申报单
- **URL**: /shipApply/tempStorage
- **Method**: POST
- **Description**: 暂存申报单信息
- **Request Body**: ShipApplyDTO
- **Response**: Standard Response Format

## 2. DTO 属性说明

### 2.1 ShipApplyDTO
| 字段名 | 中文描述 | 数据类型 | 必填状态 | 长度限制 | 备注 |
|--------|----------|----------|----------|----------|------|
| shipInfo | 船舶基本信息 | VesselShipDTO | 必填 | - | @Valid |
| vesselShipInfo | 船申报船舶业务信息 | VesselShipInfoDTO | 必填 | - | @Valid |
```

## Response Format Standardization

Ensure all response examples follow a consistent format, e.g.:
```json
{
  "flag": "T",
  "errorCode": null,
  "errorInfo": null,
  "data": {},
  "code": 200,
  "message": "Success",
  "timestamp": 1768963550,
  "success": true,
  "error": false
}
```

## Best Practices

1. **Documentation Accuracy**: Ensure all field descriptions and constraints match the actual code
2. **Consistent Formatting**: Use a standardized template for all endpoints and DTOs
3. **Nested Structures**: Clearly document nested DTOs and List<> generics
4. **Validation Rules**: Include all validation constraints from annotations
5. **Response Examples**: Provide realistic response examples for each endpoint
6. **Regular Updates**: Keep documentation in sync with code changes

## Tools Required
- Java parser to read Controller and DTO classes
- Template engine for generating documentation
- Markdown/HTML converter (if needed)

## Output Files
- `<ControllerName>接口文档.md` - API endpoint documentation
- `<ControllerName>_DTO属性文档.md` - DTO property documentation
- HTML versions (optional) for better readability

This skill automates the process of generating comprehensive API documentation, saving time and ensuring consistency across the project.