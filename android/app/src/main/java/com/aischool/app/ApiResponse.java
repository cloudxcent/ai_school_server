package com.aischool.app;

import com.google.gson.annotations.SerializedName;
import java.util.List;

public class ApiResponse {
    @SerializedName("message")
    private String message;
    
    @SerializedName("token")
    private String token;
    
    @SerializedName("user")
    private UserProfile user;
    
    @SerializedName("profiles")
    private List<KidProfile> profiles;
    
    @SerializedName("profile")
    private KidProfile profile;
    
    @SerializedName("count")
    private int count;
    
    @SerializedName("status")
    private String status;

    // Getters
    public String getMessage() { return message; }
    public String getToken() { return token; }
    public UserProfile getUser() { return user; }
    public List<KidProfile> getProfiles() { return profiles; }
    public KidProfile getProfile() { return profile; }
    public int getCount() { return count; }
    public String getStatus() { return status; }

    public static class UserProfile {
        @SerializedName("email")
        private String email;
        
        @SerializedName("full_name")
        private String fullName;
        
        @SerializedName("phone_number")
        private String phoneNumber;
        
        @SerializedName("created_at")
        private String createdAt;

        // Getters
        public String getEmail() { return email; }
        public String getFullName() { return fullName; }
        public String getPhoneNumber() { return phoneNumber; }
        public String getCreatedAt() { return createdAt; }
    }
}
