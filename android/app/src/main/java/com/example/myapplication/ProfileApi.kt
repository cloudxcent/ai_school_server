package com.example.myapplication

import retrofit2.Call
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.Header
import retrofit2.http.POST

// Data class for a single profile
data class KidProfile(
    val id: String,
    val name: String,
    val age: Int,
    val grade: String
)

// Data class for the API response
data class ProfilesResponse(
    val count: Int,
    val profiles: List<KidProfile>
)

// Retrofit API interface
interface ProfileApi {
    @GET("/api/profiles")
    fun getProfiles(@Header("Authorization") token: String): Call<ProfilesResponse>
}

// Data class for login request
data class LoginRequest(
    val email: String? = null,
    val username: String? = null,
    val password: String
)

// Data class for login response
// Assuming the response contains a 'token' field
// Add other fields if needed
data class LoginResponse(
    val token: String
)

interface AuthApi {
    @POST("/api/auth/login") // Changed to /api/auth/login for consistency with profiles endpoint
    fun login(@Body loginRequest: LoginRequest): Call<LoginResponse>
}
