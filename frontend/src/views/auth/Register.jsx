import React, { useState } from "react";
import Header from "../partials/Header";
import Footer from "../partials/Footer";
import { useParams, Link, useNavigate } from "react-router-dom";

import apiInstance from "../../utils/axios";
import { useAuthStore } from "../../store/auth";
import { register } from "../../utils/auth";

function Register() {
    const [bioData, setBioData] = useState({ fullname: "", email: "", password: "", password2: "" });
    const [isLoading, setIsLoading] = useState(false);
    //Ceci est une fonction de sélection qui prend l'état actuel du store (state) et retourne la propriété isLoggedIn. Elle permet de lire seulement la partie de l'état qui nous intéresse (ici, isLoggedIn), et d'obtenir sa valeur actuelle.
    const isLoggedIn = useAuthStore((state) => state.isLoggedIn);
    const navigate = useNavigate();


   
    const handleBioDataChange = (event) => {
        setBioData({
            ...bioData,
            [event.target.name]: event.target.value,
        });
    };

    const resetForm = () => {
        setBioData({
            fullname: "",
            email: "",
            password: "",
            password2: "",
        });
    };

    const handleRegister = async (e) => {
        e.preventDefault(); // Cette méthode est utilisée pour empêcher le comportement par défaut de l'événement, qui, dans le cas d'un formulaire, est de recharger la page après la soumission.
        setIsLoading(true);


        // La syntaxe { error } destructure l'objet retourné par register pour accéder directement à la propriété error.
        const { error } = await register(bioData.fullname, bioData.email, bioData.password, bioData.password2);
        if (error) {
            alert(JSON.stringify(error));
            resetForm();
        } else {
            navigate("/");//Redirection : Si l'enregistrement réussit (pas d'erreur), l'utilisateur est redirigé vers la page d'accueil ou une autre page désignée (représentée ici par "/")
        }

        // Reset isLoading to false when the operation is complete
        setIsLoading(false);
    };

    return (
        <>
            <Header />
            <section className="container d-flex flex-column vh-100" style={{ marginTop: "150px" }}>
                <div className="row align-items-center justify-content-center g-0 h-lg-100 py-8">
                    <div className="col-lg-5 col-md-8 py-8 py-xl-0">
                        <div className="card shadow">
                            <div className="card-body p-6">
                                <div className="mb-4">
                                    <h1 className="mb-1 fw-bold">Sign up</h1>
                                    <span>
                                        Already have an account?
                                        <Link to="/login/" className="ms-1">
                                            Sign In
                                        </Link>
                                    </span>
                                </div>
                                {/* Form */}
                                <form className="needs-validation" onSubmit={handleRegister}>
                                    {/* Username */}
                                    <div className="mb-3">
                                        <label htmlFor="email" className="form-label">
                                            Full Name
                                        </label>
                                        <input type="text" onChange={handleBioDataChange} value={bioData.fullname} id="fullname" className="form-control" name="fullname" placeholder="Enter your Name " required="" />
                                    </div>
                                    <div className="mb-3">
                                        <label htmlFor="email" className="form-label">
                                            Email Address
                                        </label>
                                        <input type="email" onChange={handleBioDataChange} value={bioData.email} id="email" className="form-control" name="email" placeholder="Enter your Email" required="" />
                                    </div>

                                    {/* Password */}
                                    <div className="mb-3">
                                        <label htmlFor="password" className="form-label">
                                            Password
                                        </label>
                                        <input type="password" onChange={handleBioDataChange} value={bioData.password} id="password" className="form-control" name="password" placeholder="**************" required="" />
                                    </div>
                                    <div className="mb-3">
                                        <label htmlFor="password" className="form-label">
                                            Confirm Password
                                        </label>
                                        <input type="password" onChange={handleBioDataChange} value={bioData.password2} id="password" className="form-control" name="password2" placeholder="**************" required="" />
                                    </div>
                                    <div>
                                        <div className="d-grid">
                                            <button className="btn btn-primary w-100" type="submit" disabled={isLoading}>
                                                {isLoading ? (
                                                    <>
                                                        <span className="mr-2 ">Processing...</span>
                                                        <i className="fas fa-spinner fa-spin" />
                                                    </>
                                                ) : (
                                                    <>
                                                        <span className="mr-2">Sign Up</span>
                                                        <i className="fas fa-user-plus" />
                                                    </>
                                                )}
                                            </button>
                                        </div>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
            <Footer />
        </>
    );
}

export default Register;
