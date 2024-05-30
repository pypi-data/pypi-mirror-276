# Celitech Python SDK 1.1.59

A Python SDK for Celitech.

- API version: 1.1.0
- SDK version: 1.1.59

Welcome to the CELITECH API documentation! Useful links: [Homepage](https://www.celitech.com) | [Support email](mailto:support@celitech.com) | [Blog](https://www.celitech.com/blog/)

## Table of Contents

- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Services](#services)

## Installation

```bash
pip install celitech-sdk
```

## Environment Variables

You will need the following environment variables in order to access all the features of this SDK:

| Name          | Description             |
| :------------ | :---------------------- |
| CLIENT_ID     | Client ID parameter     |
| CLIENT_SECRET | Client Secret parameter |

You can set these environment variables on the command line or you can use whatever tooling your project has in place to manage environment variables. If you are using a `.env` file, we have provided a template with the variable names in the `.env.example` file in the same directory as this readme.

## Services

A list of all SDK services. Click on the service name to access its corresponding service methods.

| Service                                     |
| :------------------------------------------ |
| [DestinationsService](#destinationsservice) |
| [PackagesService](#packagesservice)         |
| [PurchasesService](#purchasesservice)       |
| [ESimService](#esimservice)                 |

### DestinationsService

A list of all methods in the `DestinationsService` service. Click on the method name to view detailed information about that method.

| Methods                                 | Description              |
| :-------------------------------------- | :----------------------- |
| [list_destinations](#list_destinations) | Name of the destinations |

#### **list_destinations**

Name of the destinations

- HTTP Method: `GET`
- Endpoint: `/destinations`

**Parameters**

| Name | Type | Required | Description |
| :--- | :--- | :------: | :---------- |

**Return Type**

`ListDestinationsOkResponse`

**Example Usage Code Snippet**

```py
from celitech import Celitech, Environment

sdk = Celitech(
    base_url=Environment.DEFAULT.value
)

result = sdk.destinations.list_destinations()

print(result)
```

### PackagesService

A list of all methods in the `PackagesService` service. Click on the method name to view detailed information about that method.

| Methods                         | Description                |
| :------------------------------ | :------------------------- |
| [list_packages](#list_packages) | List of available packages |

#### **list_packages**

List of available packages

- HTTP Method: `GET`
- Endpoint: `/packages`

**Parameters**

| Name         | Type  | Required | Description                                                                                                                                                                                                         |
| :----------- | :---- | :------: | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| destination  | str   |    ❌    | ISO representation of the package's destination.                                                                                                                                                                    |
| start_date   | str   |    ❌    | Start date of the package's validity in the format 'yyyy-MM-dd'. This date can be set to the current day or any day within the next 12 months.                                                                      |
| end_date     | str   |    ❌    | End date of the package's validity in the format 'yyyy-MM-dd'. End date can be maximum 90 days after Start date.                                                                                                    |
| after_cursor | str   |    ❌    | To get the next batch of results, use this parameter. It tells the API where to start fetching data after the last item you received. It helps you avoid repeats and efficiently browse through large sets of data. |
| limit        | float |    ❌    | Maximum number of packages to be returned in the response. The value must be greater than 0 and less than or equal to 160. If not provided, the default value is 20                                                 |
| start_time   | int   |    ❌    | Epoch value representing the start time of the package's validity. This timestamp can be set to the current time or any time within the next 12 months                                                              |
| end_time     | int   |    ❌    | Epoch value representing the end time of the package's validity. End time can be maximum 90 days after Start time                                                                                                   |
| duration     | float |    ❌    | Duration in seconds for the package's validity. If this parameter is present, it will override the startTime and endTime parameters. The maximum duration for a package's validity period is 90 days                |

**Return Type**

`ListPackagesOkResponse`

**Example Usage Code Snippet**

```py
from celitech import Celitech, Environment

sdk = Celitech(
    base_url=Environment.DEFAULT.value
)

result = sdk.packages.list_packages()

print(result)
```

### PurchasesService

A list of all methods in the `PurchasesService` service. Click on the method name to view detailed information about that method.

| Methods                                               | Description                                                                                                                                                                                                                                                                                                            |
| :---------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [list_purchases](#list_purchases)                     | This endpoint can be used to list all the successful purchases made between a given interval.                                                                                                                                                                                                                          |
| [create_purchase](#create_purchase)                   | This endpoint is used to purchase a new eSIM by providing the package details.                                                                                                                                                                                                                                         |
| [top_up_esim](#top_up_esim)                           | This endpoint is used to top-up an eSIM with the previously associated destination by providing an existing ICCID and the package details. The top-up is not feasible for eSIMs in "DELETED" or "ERROR" state.                                                                                                         |
| [edit_purchase](#edit_purchase)                       | This endpoint allows you to modify the dates of an existing package with a future activation start time. Editing can only be performed for packages that have not been activated, and it cannot change the package size. The modification must not change the package duration category to ensure pricing consistency. |
| [get_purchase_consumption](#get_purchase_consumption) | This endpoint can be called for consumption notifications (e.g. every 1 hour or when the user clicks a button). It returns the data balance (consumption) of purchased packages.                                                                                                                                       |

#### **list_purchases**

This endpoint can be used to list all the successful purchases made between a given interval.

- HTTP Method: `GET`
- Endpoint: `/purchases`

**Parameters**

| Name         | Type  | Required | Description                                                                                                                                                                                                         |
| :----------- | :---- | :------: | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| iccid        | str   |    ❌    | ID of the eSIM                                                                                                                                                                                                      |
| after_date   | str   |    ❌    | Start date of the interval for filtering purchases in the format 'yyyy-MM-dd'                                                                                                                                       |
| before_date  | str   |    ❌    | End date of the interval for filtering purchases in the format 'yyyy-MM-dd'                                                                                                                                         |
| after_cursor | str   |    ❌    | To get the next batch of results, use this parameter. It tells the API where to start fetching data after the last item you received. It helps you avoid repeats and efficiently browse through large sets of data. |
| limit        | float |    ❌    | Maximum number of purchases to be returned in the response. The value must be greater than 0 and less than or equal to 100. If not provided, the default value is 20                                                |
| after        | float |    ❌    | Epoch value representing the start of the time interval for filtering purchases                                                                                                                                     |
| before       | float |    ❌    | Epoch value representing the end of the time interval for filtering purchases                                                                                                                                       |

**Return Type**

`ListPurchasesOkResponse`

**Example Usage Code Snippet**

```py
from celitech import Celitech, Environment

sdk = Celitech(
    base_url=Environment.DEFAULT.value
)

result = sdk.purchases.list_purchases()

print(result)
```

#### **create_purchase**

This endpoint is used to purchase a new eSIM by providing the package details.

- HTTP Method: `POST`
- Endpoint: `/purchases`

**Parameters**

| Name         | Type                  | Required | Description       |
| :----------- | :-------------------- | :------: | :---------------- |
| request_body | CreatePurchaseRequest |    ✅    | The request body. |

**Return Type**

`CreatePurchaseOkResponse`

**Example Usage Code Snippet**

```py
from celitech import Celitech, Environment
from celitech.models import CreatePurchaseRequest

sdk = Celitech(
    base_url=Environment.DEFAULT.value
)

request_body = CreatePurchaseRequest(
    destination="FRA",
    data_limit_in_gb=1,
    start_date="2023-11-01",
    end_date="2023-11-20"
)

result = sdk.purchases.create_purchase(request_body=request_body)

print(result)
```

#### **top_up_esim**

This endpoint is used to top-up an eSIM with the previously associated destination by providing an existing ICCID and the package details. The top-up is not feasible for eSIMs in "DELETED" or "ERROR" state.

- HTTP Method: `POST`
- Endpoint: `/purchases/topup`

**Parameters**

| Name         | Type             | Required | Description       |
| :----------- | :--------------- | :------: | :---------------- |
| request_body | TopUpEsimRequest |    ✅    | The request body. |

**Return Type**

`TopUpEsimOkResponse`

**Example Usage Code Snippet**

```py
from celitech import Celitech, Environment
from celitech.models import TopUpEsimRequest

sdk = Celitech(
    base_url=Environment.DEFAULT.value
)

request_body = TopUpEsimRequest(
    iccid="1111222233334444555",
    data_limit_in_gb=1,
    start_date="2023-11-01",
    end_date="2023-11-20"
)

result = sdk.purchases.top_up_esim(request_body=request_body)

print(result)
```

#### **edit_purchase**

This endpoint allows you to modify the dates of an existing package with a future activation start time. Editing can only be performed for packages that have not been activated, and it cannot change the package size. The modification must not change the package duration category to ensure pricing consistency.

- HTTP Method: `POST`
- Endpoint: `/purchases/edit`

**Parameters**

| Name         | Type                | Required | Description       |
| :----------- | :------------------ | :------: | :---------------- |
| request_body | EditPurchaseRequest |    ✅    | The request body. |

**Return Type**

`EditPurchaseOkResponse`

**Example Usage Code Snippet**

```py
from celitech import Celitech, Environment
from celitech.models import EditPurchaseRequest

sdk = Celitech(
    base_url=Environment.DEFAULT.value
)

request_body = EditPurchaseRequest(
    purchase_id="ae471106-c8b4-42cf-b83a-b061291f2922",
    start_date="2023-11-01",
    end_date="2023-11-20"
)

result = sdk.purchases.edit_purchase(request_body=request_body)

print(result)
```

#### **get_purchase_consumption**

This endpoint can be called for consumption notifications (e.g. every 1 hour or when the user clicks a button). It returns the data balance (consumption) of purchased packages.

- HTTP Method: `GET`
- Endpoint: `/purchases/{purchaseId}/consumption`

**Parameters**

| Name        | Type | Required | Description        |
| :---------- | :--- | :------: | :----------------- |
| purchase_id | str  |    ✅    | ID of the purchase |

**Return Type**

`GetPurchaseConsumptionOkResponse`

**Example Usage Code Snippet**

```py
from celitech import Celitech, Environment

sdk = Celitech(
    base_url=Environment.DEFAULT.value
)

result = sdk.purchases.get_purchase_consumption(purchase_id="4973fa15-6979-4daa-9cf3-672620df819c")

print(result)
```

### ESimService

A list of all methods in the `ESimService` service. Click on the method name to view detailed information about that method.

| Methods                               | Description                            |
| :------------------------------------ | :------------------------------------- |
| [get_esim](#get_esim)                 | Get status from eSIM                   |
| [get_esim_device](#get_esim_device)   | Get device info from an installed eSIM |
| [get_esim_history](#get_esim_history) | Get history from an eSIM               |
| [get_esim_mac](#get_esim_mac)         | Get MAC from eSIM                      |

#### **get_esim**

Get status from eSIM

- HTTP Method: `GET`
- Endpoint: `/esim`

**Parameters**

| Name  | Type | Required | Description    |
| :---- | :--- | :------: | :------------- |
| iccid | str  |    ✅    | ID of the eSIM |

**Return Type**

`GetEsimOkResponse`

**Example Usage Code Snippet**

```py
from celitech import Celitech, Environment

sdk = Celitech(
    base_url=Environment.DEFAULT.value
)

result = sdk.e_sim.get_esim(iccid="1111222233334444555")

print(result)
```

#### **get_esim_device**

Get device info from an installed eSIM

- HTTP Method: `GET`
- Endpoint: `/esim/{iccid}/device`

**Parameters**

| Name  | Type | Required | Description    |
| :---- | :--- | :------: | :------------- |
| iccid | str  |    ✅    | ID of the eSIM |

**Return Type**

`GetEsimDeviceOkResponse`

**Example Usage Code Snippet**

```py
from celitech import Celitech, Environment

sdk = Celitech(
    base_url=Environment.DEFAULT.value
)

result = sdk.e_sim.get_esim_device(iccid="1111222233334444555")

print(result)
```

#### **get_esim_history**

Get history from an eSIM

- HTTP Method: `GET`
- Endpoint: `/esim/{iccid}/history`

**Parameters**

| Name  | Type | Required | Description    |
| :---- | :--- | :------: | :------------- |
| iccid | str  |    ✅    | ID of the eSIM |

**Return Type**

`GetEsimHistoryOkResponse`

**Example Usage Code Snippet**

```py
from celitech import Celitech, Environment

sdk = Celitech(
    base_url=Environment.DEFAULT.value
)

result = sdk.e_sim.get_esim_history(iccid="1111222233334444555")

print(result)
```

#### **get_esim_mac**

Get MAC from eSIM

- HTTP Method: `GET`
- Endpoint: `/esim/{iccid}/mac`

**Parameters**

| Name  | Type | Required | Description    |
| :---- | :--- | :------: | :------------- |
| iccid | str  |    ✅    | ID of the eSIM |

**Return Type**

`GetEsimMacOkResponse`

**Example Usage Code Snippet**

```py
from celitech import Celitech, Environment

sdk = Celitech(
    base_url=Environment.DEFAULT.value
)

result = sdk.e_sim.get_esim_mac(iccid="1111222233334444555")

print(result)
```
