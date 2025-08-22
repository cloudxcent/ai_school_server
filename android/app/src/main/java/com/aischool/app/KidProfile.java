package com.aischool.app;

import com.google.gson.annotations.SerializedName;

public class KidProfile {
    @SerializedName("id")
    private String id;
    
    @SerializedName("name")
    private String name;
    
    @SerializedName("age")
    private int age;
    
    @SerializedName("grade")
    private String grade;
    
    @SerializedName("avatar")
    private String avatar;
    
    @SerializedName("learning_goals")
    private String learningGoals;
    
    @SerializedName("progress")
    private String progress;
    
    @SerializedName("created_at")
    private String createdAt;
    
    @SerializedName("last_activity")
    private String lastActivity;

    // Constructors
    public KidProfile() {}

    public KidProfile(String name, int age, String grade, String avatar, String learningGoals) {
        this.name = name;
        this.age = age;
        this.grade = grade;
        this.avatar = avatar;
        this.learningGoals = learningGoals;
    }

    // Getters and Setters
    public String getId() { return id; }
    public void setId(String id) { this.id = id; }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public int getAge() { return age; }
    public void setAge(int age) { this.age = age; }

    public String getGrade() { return grade; }
    public void setGrade(String grade) { this.grade = grade; }

    public String getAvatar() { return avatar; }
    public void setAvatar(String avatar) { this.avatar = avatar; }

    public String getLearningGoals() { return learningGoals; }
    public void setLearningGoals(String learningGoals) { this.learningGoals = learningGoals; }

    public String getProgress() { return progress; }
    public void setProgress(String progress) { this.progress = progress; }

    public String getCreatedAt() { return createdAt; }
    public void setCreatedAt(String createdAt) { this.createdAt = createdAt; }

    public String getLastActivity() { return lastActivity; }
    public void setLastActivity(String lastActivity) { this.lastActivity = lastActivity; }

    @Override
    public String toString() {
        return "KidProfile{" +
                "id='" + id + '\'' +
                ", name='" + name + '\'' +
                ", age=" + age +
                ", grade='" + grade + '\'' +
                ", avatar='" + avatar + '\'' +
                ", learningGoals='" + learningGoals + '\'' +
                '}';
    }
}
