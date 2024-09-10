import { BrowserRouter, Route, Routes } from "react-router-dom"
import Layout from "./layout/Layout"
import Home from "./pages/Home"
import { Button } from "./components/ui/button"


function App() {


  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout></Layout>}>
           <Route index element={<Home></Home>}></Route>
        </Route>
      </Routes>
    </BrowserRouter>

  )
}

export default App
