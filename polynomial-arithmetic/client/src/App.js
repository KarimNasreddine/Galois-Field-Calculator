import { React, useState } from "react";
import "./App.css";
import {
  Typography,
  TextField,
  Select,
  Button,
  MenuItem,
} from "@material-ui/core";

var SERVER_URL = "https://polynomial-arithmetic.herokuapp.com/";

// offline testing
// var SERVER_URL = "http://127.0.0.1:5000";

function App() {
  const [firstOperand, setFirstOperand] = useState("");
  const [secondOperand, setSecondOperand] = useState("");
  const [thirdOperand, setThirdOperand] = useState("");
  const [forthOperand, setForthOperand] = useState("");
  const [operation, setOperation] = useState("+");
  const [operationsResult, setOperationsResult] = useState("");
  const [inverseResult, setInverseResult] = useState("");
  const [moduloResult, setModuloResult] = useState("");

  function getPolyOperations() {
    return fetch(`${SERVER_URL}/getPolyOperations`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        firstOperand: firstOperand,
        secondOperand: secondOperand,
        operation: operation,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (
          typeof data.result === "string" ||
          data.result instanceof String ||
          data.result !== ""
        ) {
          if (data.result === "") {
            setOperationsResult("0");
          } else {
            setOperationsResult(data.result);
          }
        } else {
          setOperationsResult("Please enter a valid polynomial");
        }
      });
  }

  function getPolyInverse() {
    return fetch(`${SERVER_URL}/getPolyInverse`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        thirdOperand: thirdOperand,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (
          typeof data.result === "string" ||
          data.result instanceof String ||
          data.result !== ""
        ) {
          if (data.result === "") {
            setInverseResult("0");
          } else {
            setInverseResult(data.result);
          }
        } else {
          setInverseResult("Please enter a valid polynomial");
        }
      });
  }

  function getPolyModulo() {
    return fetch(`${SERVER_URL}/getPolyModulo`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        forthOperand: forthOperand,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (
          typeof data.result === "string" ||
          data.result instanceof String ||
          data.result !== ""
        ) {
          if (data.result === "") {
            setModuloResult("0");
          } else {
            setModuloResult(data.result);
          }
        } else {
          setModuloResult("Please enter a valid polynomial");
        }
      });
  }

  return (
    <div>
      <div
        style={{
          width: "100%",
          textAlign: "center",
          backgroundColor: "white",
          position: "Sticky",
          top: "0",
          boxShadow:
            "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)",
          zIndex: "1",
        }}
      >
        <Typography
          variant="h3"
          style={{ color: "#3f51b5", padding: "0.3em", fontWeight: "bold" }}
        >
          Galois Field Calculator
        </Typography>
      </div>
      <div className="wrapper">
        <Typography variant="h4" style={{ color: "#3f51b5" }}>
          Polynomial Arithmetic Operations
        </Typography>
        <Typography variant="h6" gutterBottom style={{ fontWeight: "300" }}>
          Note: All results are modulo GF(2^163) and maximum power of x is 499
        </Typography>
        <Typography
          variant="subtitle1"
          style={{ color: "#3f51b5" }}
          gutterBottom
        >
          Please enter the polynomials in the following format: x^43 + x^21 +
          ... + x + 1 as an example.
        </Typography>
        <form name="transaction-entry">
          <div className="amount-input">
            <TextField
              id="first-polynomial"
              label="First Polynomial"
              type="string"
              value={firstOperand}
              style={{ width: "100%" }}
              onChange={({ target: { value } }) => setFirstOperand(value)}
            />
          </div>
          <div className="amount-input">
            <TextField
              id="second-polynomial"
              label="Second Polynomial"
              type="string"
              value={secondOperand}
              style={{ width: "100%" }}
              onChange={({ target: { value } }) => setSecondOperand(value)}
            />
          </div>
          <div className="button-container">
            <Select
              id="transaction-type"
              defaultValue={operation}
              size="small"
              onChange={({ target: { value } }) => setOperation(value)}
            >
              <MenuItem value="+">Addition</MenuItem>
              <MenuItem value="-">Subtraction</MenuItem>
              <MenuItem value="*">Multiplication</MenuItem>
              <MenuItem value="/">Division</MenuItem>
            </Select>
            <Button
              id="calculate-button"
              className="button"
              type="button"
              onClick={getPolyOperations}
              size="medium"
              style={{
                marginLeft: "10px",
              }}
              color="primary"
              variant="outlined"
            >
              Calculate
            </Button>
          </div>
          <Typography
            variant="h5"
            gutterBottom
            style={{ overflowWrap: "break-word", marginTop: "1em" }}
          >
            <span style={{ color: "#3f51b5", fontWeight: "bold" }}>
              Result:
            </span>{" "}
            {operationsResult}
          </Typography>
        </form>
      </div>
      <div className="wrapper">
        <Typography variant="h4" style={{ color: "#3f51b5" }}>
          Polynomial Arithmetic Inverse
        </Typography>
        <Typography variant="h6" gutterBottom style={{ fontWeight: "300" }}>
          Note: All results are modulo GF(2^163) and maximum power of x is 499
        </Typography>
        <Typography
          variant="subtitle1"
          style={{ color: "#3f51b5" }}
          gutterBottom
        >
          Please enter the polynomials in the following format: x^43 + x^21 +
          ... + x + 1 as an example.
        </Typography>
        <form name="transaction-entry">
          <div className="amount-input">
            <TextField
              id="third-polynomial"
              label="Enter Polynomial"
              type="string"
              value={thirdOperand}
              style={{ width: "100%" }}
              onChange={({ target: { value } }) => setThirdOperand(value)}
            />
          </div>
          <div className="button-container">
            <Button
              id="calculate-button"
              className="button"
              type="button"
              onClick={getPolyInverse}
              size="medium"
              color="primary"
              variant="outlined"
            >
              Calculate
            </Button>
          </div>
          <Typography
            variant="h5"
            gutterBottom
            style={{ overflowWrap: "break-word", marginTop: "1em" }}
          >
            <span style={{ color: "#3f51b5", fontWeight: "bold" }}>
              Result:
            </span>{" "}
            {inverseResult}
          </Typography>
        </form>
      </div>
      <div className="wrapper">
        <Typography variant="h4" style={{ color: "#3f51b5" }}>
          Polynomial Arithmetic Reduction
        </Typography>
        <Typography variant="h6" gutterBottom style={{ fontWeight: "300" }}>
          Note: All results are modulo GF(2^163) and maximum power of x is 499
        </Typography>
        <Typography
          variant="subtitle1"
          style={{ color: "#3f51b5" }}
          gutterBottom
        >
          Please enter a polynomial of degree larger than 163 to show its
          reduction in GF(2^163):
        </Typography>
        <form name="transaction-entry">
          <div className="amount-input">
            <TextField
              id="forth-polynomial"
              label="Enter Polynomial"
              type="string"
              value={forthOperand}
              style={{ width: "100%" }}
              onChange={({ target: { value } }) => setForthOperand(value)}
            />
          </div>
          <div className="button-container">
            <Button
              id="calculate-button"
              className="button"
              type="button"
              onClick={getPolyModulo}
              size="medium"
              color="primary"
              variant="outlined"
            >
              Calculate
            </Button>
          </div>
          <Typography
            variant="h5"
            gutterBottom
            style={{ overflowWrap: "break-word", marginTop: "1em" }}
          >
            <span style={{ color: "#3f51b5", fontWeight: "bold" }}>
              Result:
            </span>{" "}
            {moduloResult}
          </Typography>
        </form>
      </div>
    </div>
  );
}

export default App;
