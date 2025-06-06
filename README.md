# QR Sheet Generator API

This is a Flask API that accepts a list of data in JSON format and returns an A4-style PNG sheet containing up to 50 QR codes.

### Endpoint:
POST `/generate_sheet`

### Input:
```json
{
  "data": [
    {
      "X1": "Name1",
      "X2": "Desc1",
      "X3": "Misc1",
      "X4": ["XMisc1", "YMisc1"],
      "X5": "RMisc1"
    },
    ...
  ]
}
```

### Output:
Returns a PNG image of QR codes arranged in a 5x10 grid (fits A4 size).
