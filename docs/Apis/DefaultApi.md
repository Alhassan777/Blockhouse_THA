# DefaultApi

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**createTradeOrderOrdersPost**](DefaultApi.md#createTradeOrderOrdersPost) | **POST** /orders | Create Trade Order |
| [**getTradeOrderOrdersOrderIdGet**](DefaultApi.md#getTradeOrderOrdersOrderIdGet) | **GET** /orders/{order_id} | Get Trade Order |
| [**getTradeOrdersOrdersGet**](DefaultApi.md#getTradeOrdersOrdersGet) | **GET** /orders | Get Trade Orders |
| [**rootGet**](DefaultApi.md#rootGet) | **GET** / | Root |


<a name="createTradeOrderOrdersPost"></a>
# **createTradeOrderOrdersPost**
> Order createTradeOrderOrdersPost(OrderCreate)

Create Trade Order

    Create a new trade order and broadcast a notification.  Args:     order (schemas.OrderCreate): The order data to create     db (Session): The database session  Returns:     models.Order: The created order

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **OrderCreate** | [**OrderCreate**](../Models/OrderCreate.md)|  | |

### Return type

[**Order**](../Models/Order.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

<a name="getTradeOrderOrdersOrderIdGet"></a>
# **getTradeOrderOrdersOrderIdGet**
> Order getTradeOrderOrdersOrderIdGet(order\_id)

Get Trade Order

    Retrieve a specific trade order by ID.  Args:     order_id (int): The ID of the order to retrieve     db (Session): The database session  Returns:     models.Order: The requested order  Raises:     HTTPException: If the order is not found

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **order\_id** | **Integer**|  | [default to null] |

### Return type

[**Order**](../Models/Order.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="getTradeOrdersOrdersGet"></a>
# **getTradeOrdersOrdersGet**
> List getTradeOrdersOrdersGet(skip, limit)

Get Trade Orders

    Retrieve a list of trade orders with pagination.  Args:     skip (int): Number of records to skip     limit (int): Maximum number of records to return     db (Session): The database session  Returns:     List[models.Order]: List of orders

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **skip** | **Integer**|  | [optional] [default to 0] |
| **limit** | **Integer**|  | [optional] [default to 100] |

### Return type

[**List**](../Models/Order.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="rootGet"></a>
# **rootGet**
> oas_any_type_not_mapped rootGet()

Root

    Root endpoint that returns a welcome message.  Returns:     dict: A welcome message for the API

### Parameters
This endpoint does not need any parameter.

### Return type

[**oas_any_type_not_mapped**](../Models/AnyType.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

