package com.aischool.app;

import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.DELETE;
import retrofit2.http.GET;
import retrofit2.http.Header;
import retrofit2.http.POST;
import retrofit2.http.PUT;
import retrofit2.http.Path;

public interface ApiService {
    
    // Health check
    @GET("health")
    Call<ApiResponse> healthCheck();
    
    // Authentication endpoints
    @POST("auth/register")
    Call<ApiResponse> register(@Body User user);
    
    @POST("auth/login")
    Call<ApiResponse> login(@Body User user);
    
    @GET("auth/user")
    Call<ApiResponse> getUser(@Header("Authorization") String authorization);
    
    @POST("auth/logout")
    Call<ApiResponse> logout(@Header("Authorization") String authorization);
    
    // Kids Profiles endpoints
    @GET("profiles")
    Call<ApiResponse> getProfiles(@Header("Authorization") String authorization);
    
    @POST("profiles")
    Call<ApiResponse> createProfile(@Header("Authorization") String authorization, @Body KidProfile profile);
    
    @GET("profiles/{id}")
    Call<ApiResponse> getProfile(@Header("Authorization") String authorization, @Path("id") String profileId);
    
    @PUT("profiles/{id}")
    Call<ApiResponse> updateProfile(@Header("Authorization") String authorization, @Path("id") String profileId, @Body KidProfile profile);
    
    @DELETE("profiles/{id}")
    Call<ApiResponse> deleteProfile(@Header("Authorization") String authorization, @Path("id") String profileId);
}
