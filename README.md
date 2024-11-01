# Guests API

This API allows you to manage and edit a drinks database in SQLite. You can perform CRUD operations such as create, retrieve, update and delete.

## Endpoints

- **GET /drinks**  
  Retrieves a list of all drinks and their respective information.

  **Response**:  
  - `200 OK` with a JSON array of guests:
    ```json
    [
        {
            "drink_id": 1,
            "drink_name": "Mai Tai",
            "category": "Cocktail",
            "price": "170",
            "sale_count": 2360
        },
        ...
    ]
    ```
  - If no drinks are found, returns an empty array: `[]`.

- **POST /guests**  
  Adds a new drink to the database.

  **Request Body**:
  ```json
  {
      "drink_id": 11,
      "drink_name": "White Russia ",
      "category": "Cocktail",
      "price": "160",
      "sale_count": 0
  }

**Response**:  
- `201 Created` with the newly created drink:
  ```json
  [
      {
          "drink_id": 11,
          "drink_name": "White Russia ",
          "category": "Cocktail",
          "price": "160",
          "sale_count": 0
      },
      ...
  ]
  ```
-

- **GET /drinks/int:id**  
  Retrieves a specific drink by their drink ID.

  **Response**:  
  - `200 OK` with guest details:
    ```json
    [
        {
          "drink_id": 11,
          "drink_name": "White Russia ",
          "category": "Cocktail",
          "price": "160",
          "sale_count": 0
        },
        ...
    ]
    ```
  - `404 Not Found` if the drink does not exist.

  - **DELETE /drinks/int:id**  
  Deletes a drink by their drink ID.

  **Response**:  
  - `204 No Content` if the deletion is successful.
  - `404 Not Found` if the drink does not exist

  - **PUT OR PATCH /drinks/int:id**  
  Updates the details of a drink

  **Request Body**:
  ```json
  {
      "drink_id": 11,
      "drink_name": "White Russia ",
      "category": "Cocktail",
      "price": "160",
      "sale_count": 0
  }
  
**Response**:  
- `200 OK` with a success message if updated successfully:
  ```json
  [
      {
          "message": "Drink updated successfully"
      },
      ...
  ]
  ```
- `404 Not Found` if the drink does not exist.
