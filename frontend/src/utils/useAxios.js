import axios from 'axios';
import { getRefreshToken, isAccessTokenExpired, setAuthUser } from './auth'; // Import authentication-related functions
import { API_BASE_URL } from './constants'; // Import the base API URL
import Cookies from 'js-cookie'; // Import the 'js-cookie' library for managing cookies

// Define a custom Axios instance creator function
const useAxios = () => {
    // Retrieve the access and refresh tokens from cookies
    const accessToken = Cookies.get('access_token');
    const refreshToken = Cookies.get('refresh_token');

    

    // Create an Axios instance with base URL and access token in the headers
    const axiosInstance = axios.create({
        baseURL: API_BASE_URL,
        headers: { Authorization: `Bearer ${accessToken}` },//Ajoute le token d'accès dans les en-têtes des requêtes pour l'authentification.
    });

    // Add an interceptor to the Axios instance
    // Ajoute un intercepteur de requêtes à l'instance Axios. Cet intercepteur permet de modifier les requêtes avant qu'elles ne soient envoyées.
    axiosInstance.interceptors.request.use(async (req) => {
        // Check if the access token is expired
        if (!isAccessTokenExpired(accessToken)) {
            return req; // If not expired, return the original request
        }

        // If the access token is expired, refresh it
        const response = await getRefreshToken(refreshToken);
        // console.log('Refresh Token Response:', response);
        // Update the application with the new access and refresh tokens
        setAuthUser(response.access, response.refresh);

        // Update the request's 'Authorization' header with the new access token
        req.headers.Authorization = `Bearer ${response?.data?.access}`;
        return req; // Return the updated request
    });

    return axiosInstance; // Return the custom Axios instance
};

export default useAxios; // Export the custom Axios instance creator function
