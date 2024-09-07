import { useState } from 'react'
import './App.css'
import {Route , Routes , BrowserRouter} from 'react-router-dom'
import MainWrapper from './layouts/MainWrapper'
import {
  Index,
  Detail,
  Search,
  Category,
  About,
  Contact,
  Register,
  Login,
  Logout,
  ForgotPassword,
  CreatePassword,
  Dashboard,
  Posts,
  AddPost,
  EditPost,
  Comments,
  Notifications,
  Profile
} from './views';


function App() {
  return (
    <>
      <BrowserRouter>
        <MainWrapper>
            <Routes>
                <Route path="/" element={<Index />} />
                <Route path="/:slug/" element={<Detail />} />
                <Route path="/category/:slug/" element={<Category />} />
                <Route path="/search/" element={<Search />} />

                {/* Authentication */}
                <Route path="/register/" element={<Register />} />
                <Route path="/login/" element={<Login />} />
                <Route path="/logout/" element={<Logout />} />
                <Route path="/forgot-password/" element={<ForgotPassword />} />
                <Route path="/create-password/" element={<CreatePassword />} />

                {/* Dashboard */}
                <Route path="/dashboard/" element={<Dashboard />} />
                <Route path="/posts/" element={<Posts />} />
                <Route path="/add-post/" element={<AddPost />} />
                <Route path="/edit-post/:id/" element={<EditPost />} />
                <Route path="/comments/" element={<Comments/>} />
                <Route path="/notifications/" element={<Notifications />} />
                <Route path="/profile/" element={<Profile />} />

                {/* Pages */}
                <Route path="/about/" element={<About />} />
                <Route path="/contact/" element={<Contact />} />
            </Routes>
        </MainWrapper>
      </BrowserRouter>
    </>
  )
}

export default App
