"use strict";

const display = document.querySelector("#display");
const expression = document.querySelector("#expression");
const keypad = document.querySelector(".keypad");
const clearButton = document.querySelector('[data-action="clear"]');
const operatorButtons = [...document.querySelectorAll('[data-action="operator"]')];

const operatorLabels = {
  "+": "+",
  "-": "−",
  "*": "×",
  "/": "÷"
};

const numberFormatter = new Intl.NumberFormat("en-US", {
  maximumFractionDigits: 10
});

let currentInput = "0";
let storedValue = null;
let pendingOperator = null;
let waitingForOperand = false;
let lastOperator = null;
let lastOperand = null;
let hasError = false;

function formatNumber(value) {
  if (!Number.isFinite(value)) {
    return "Error";
  }

  const roundedValue = Number(value.toPrecision(11));
  if (roundedValue === 0) {
    return "0";
  }

  if (Math.abs(roundedValue) >= 1e12 || Math.abs(roundedValue) < 1e-7) {
    return roundedValue.toExponential(5).replace(/\.?0+e/, "e");
  }

  return numberFormatter.format(roundedValue);
}

function formatEntry(value) {
  if (value.includes("e")) {
    return formatNumber(Number(value)).replace(/^-/, "−");
  }

  const isNegative = value.startsWith("-");
  const unsignedValue = isNegative ? value.slice(1) : value;
  const [integerPart, decimalPart] = unsignedValue.split(".");
  const formattedInteger = numberFormatter.format(Number(integerPart || "0"));
  const formattedValue = decimalPart === undefined
    ? formattedInteger
    : `${formattedInteger}.${decimalPart}`;

  return `${isNegative ? "−" : ""}${formattedValue}`;
}

function render() {
  display.textContent = hasError ? "Error" : formatEntry(currentInput);
  const isAllClear = currentInput === "0" && !pendingOperator;
  clearButton.textContent = isAllClear ? "AC" : "C";
  clearButton.setAttribute("aria-label", isAllClear ? "All clear" : "Clear");

  operatorButtons.forEach((button) => {
    const isSelected = button.dataset.value === pendingOperator && waitingForOperand;
    button.classList.toggle("is-selected", isSelected);
    button.setAttribute("aria-pressed", String(isSelected));
  });
}

function resetAll() {
  currentInput = "0";
  storedValue = null;
  pendingOperator = null;
  waitingForOperand = false;
  lastOperator = null;
  lastOperand = null;
  hasError = false;
  expression.textContent = "";
}

function enterDigit(digit) {
  if (hasError || waitingForOperand) {
    currentInput = digit;
    waitingForOperand = false;
    hasError = false;
  } else if (currentInput === "0") {
    currentInput = digit;
  } else if (currentInput === "-0") {
    currentInput = `-${digit}`;
  } else if (currentInput.replace(/\D/g, "").length < 12) {
    currentInput += digit;
  }
}

function enterDecimal() {
  if (hasError || waitingForOperand) {
    currentInput = "0.";
    waitingForOperand = false;
    hasError = false;
  } else if (!currentInput.includes(".")) {
    currentInput += ".";
  }
}

function calculate(left, right, operator) {
  switch (operator) {
    case "+":
      return left + right;
    case "-":
      return left - right;
    case "*":
      return left * right;
    case "/":
      return right === 0 ? NaN : left / right;
    default:
      return right;
  }
}

function showError() {
  currentInput = "0";
  storedValue = null;
  pendingOperator = null;
  waitingForOperand = true;
  lastOperator = null;
  lastOperand = null;
  hasError = true;
  expression.textContent = "Cannot divide by zero";
}

function chooseOperator(operator) {
  if (hasError) {
    resetAll();
  }

  const currentValue = Number(currentInput);
  if (pendingOperator && !waitingForOperand) {
    const result = calculate(storedValue, currentValue, pendingOperator);
    if (!Number.isFinite(result)) {
      showError();
      render();
      return;
    }
    currentInput = String(Number(result.toPrecision(11)));
  }

  storedValue = Number(currentInput);
  pendingOperator = operator;
  waitingForOperand = true;
  lastOperator = null;
  lastOperand = null;
  expression.textContent = `${formatNumber(storedValue)} ${operatorLabels[operator]}`;
}

function enterEquals() {
  if (hasError) {
    return;
  }

  if (pendingOperator) {
    const left = storedValue;
    const right = waitingForOperand ? left : Number(currentInput);
    const operator = pendingOperator;
    const result = calculate(left, right, operator);

    expression.textContent = `${formatNumber(left)} ${operatorLabels[operator]} ${formatNumber(right)} =`;
    if (!Number.isFinite(result)) {
      showError();
      render();
      return;
    }

    currentInput = String(Number(result.toPrecision(11)));
    lastOperator = operator;
    lastOperand = right;
    storedValue = null;
    pendingOperator = null;
    waitingForOperand = true;
  } else if (lastOperator) {
    const left = Number(currentInput);
    const result = calculate(left, lastOperand, lastOperator);
    expression.textContent = `${formatNumber(left)} ${operatorLabels[lastOperator]} ${formatNumber(lastOperand)} =`;

    if (!Number.isFinite(result)) {
      showError();
      render();
      return;
    }

    currentInput = String(Number(result.toPrecision(11)));
    waitingForOperand = true;
  }
}

function changeSign() {
  if (hasError) {
    return;
  }
  currentInput = currentInput.startsWith("-")
    ? currentInput.slice(1)
    : `-${currentInput}`;
}

function applyPercent() {
  if (hasError) {
    return;
  }
  currentInput = String(Number(currentInput) / 100);
  waitingForOperand = false;
}

function clear() {
  if (hasError || currentInput === "0") {
    resetAll();
  } else {
    currentInput = "0";
    waitingForOperand = Boolean(pendingOperator);
  }
}

function handleAction(action, value) {
  switch (action) {
    case "digit":
      enterDigit(value);
      break;
    case "decimal":
      enterDecimal();
      break;
    case "operator":
      chooseOperator(value);
      break;
    case "equals":
      enterEquals();
      break;
    case "sign":
      changeSign();
      break;
    case "percent":
      applyPercent();
      break;
    case "clear":
      clear();
      break;
    default:
      return;
  }

  render();
}

keypad.addEventListener("click", (event) => {
  const button = event.target.closest("button");
  if (button) {
    handleAction(button.dataset.action, button.dataset.value);
  }
});

document.addEventListener("keydown", (event) => {
  const key = event.key;
  const digit = /^[0-9]$/.test(key);
  const operator = {
    "+": "+",
    "-": "-",
    "*": "*",
    "x": "*",
    "X": "*",
    "/": "/"
  }[key];

  if (digit) {
    handleAction("digit", key);
  } else if (key === "." || key === ",") {
    handleAction("decimal");
  } else if (operator) {
    handleAction("operator", operator);
  } else if (key === "Enter" || key === "=") {
    handleAction("equals");
  } else if (key === "%") {
    handleAction("percent");
  } else if (key === "Escape" || key === "Delete") {
    handleAction("clear");
  } else if (key === "Backspace" && !hasError) {
    if (!waitingForOperand && currentInput.length > 1) {
      currentInput = currentInput.slice(0, -1);
      if (currentInput === "-") {
        currentInput = "0";
      }
    } else {
      currentInput = "0";
    }
    render();
  } else {
    return;
  }

  event.preventDefault();
});

render();
