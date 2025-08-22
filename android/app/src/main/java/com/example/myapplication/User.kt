package com.example.myapplication.model

data class User(
    val PartitionKey: String = "User", // Logical grouping, e.g., "User"
    val RowKey: String = "", // Unique user ID
    val username: String = "",
    val password: String = "",
    val email: String = "",
    val fullName: String = "",
    val dob: String = "",
    val location: String = ""
)