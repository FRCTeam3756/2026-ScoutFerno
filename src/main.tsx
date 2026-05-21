import { BrowserRouter } from "react-router-dom";
import { createRoot } from "react-dom/client";
import "./index.css";
import { App } from "./App.tsx";

const root = createRoot(document.getElementById("app")!);

root.render(
  <BrowserRouter>
    <App />
  </BrowserRouter>
);
