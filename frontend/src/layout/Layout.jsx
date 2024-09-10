import React from 'react'
import Header from '../components/Header'
import { Outlet } from 'react-router-dom'
import Footer from '../components/Footer'

function Layout() {
  return (
    <div>
        <Header></Header>
        <Outlet></Outlet>
        {/* <Footer></Footer> */}

    </div>
  )
}

export default Layout