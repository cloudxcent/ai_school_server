package com.example.myapplication

import android.app.DatePickerDialog
import android.os.Bundle
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.interaction.FocusInteraction
import androidx.compose.foundation.interaction.Interaction
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.example.myapplication.model.User
import com.example.myapplication.ui.theme.MyApplicationTheme
import java.util.Calendar
import kotlinx.coroutines.flow.collectLatest
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.POST

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MyApplicationTheme {
                val navController = rememberNavController()
                var user by remember { mutableStateOf<User?>(null) }
                NavHost(navController = navController, startDestination = "login") {
                    composable("login") { LoginScreen(navController) }
                    composable("home") { HomeScreen(navController) }
                    composable("signup") { SignupScreen(navController) }
                    composable("forgot_password") { ForgotPasswordScreen(navController) }
                    composable("profile_update") {
                        user?.let { ProfileUpdateScreen(navController, it) }
                    }
                    composable("profiles") { ProfilesScreen(navController) }
                }
            }
        }
    }
}

@Composable
fun LoginScreen(navController: NavController) {
    val context = LocalContext.current
    var username by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    var isLoading by remember { mutableStateOf(false) }
    var errorMessage by remember { mutableStateOf("") }
    var profiles by remember { mutableStateOf<List<KidProfile>?>(null) }

    // Retrofit instance
    val retrofit = Retrofit.Builder()
        .baseUrl("http://192.168.0.111:5000/") // Fixed: removed /api/ for correct endpoint resolution
        .addConverterFactory(GsonConverterFactory.create())
        .build()
    val profileApi = retrofit.create(ProfileApi::class.java)
    val authApi = retrofit.create(AuthApi::class.java)

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(32.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Image(
            painter = painterResource(id = R.drawable.company_logo),
            contentDescription = "Company Logo",
            modifier = Modifier.size(120.dp)
        )
        Spacer(modifier = Modifier.height(32.dp))

        OutlinedTextField(
            value = username,
            onValueChange = { username = it },
            label = { Text("Username") },
            modifier = Modifier.fillMaxWidth()
        )
        Spacer(modifier = Modifier.height(16.dp))

        OutlinedTextField(
            value = password,
            onValueChange = { password = it },
            label = { Text("Password") },
            visualTransformation = PasswordVisualTransformation(),
            modifier = Modifier.fillMaxWidth()
        )
        Spacer(modifier = Modifier.height(24.dp))

        Button(
            onClick = {
                isLoading = true
                errorMessage = ""
                // Call login API first
                val loginRequest = if (username.contains("@")) {
                    LoginRequest(email = username, password = password)
                } else {
                    LoginRequest(username = username, password = password)
                }
                authApi.login(loginRequest).enqueue(object : Callback<LoginResponse> {
                    override fun onResponse(call: Call<LoginResponse>, response: Response<LoginResponse>) {
                        isLoading = false
                        when (response.code()) {
                            200 -> {
                                val token = response.body()?.token
                                if (token != null) {
                                    // Now call profiles API with token
                                    profileApi.getProfiles("Bearer $token").enqueue(object : Callback<ProfilesResponse> {
                                        override fun onResponse(call: Call<ProfilesResponse>, response: Response<ProfilesResponse>) {
                                            if (response.isSuccessful) {
                                                profiles = response.body()?.profiles
                                                navController.currentBackStackEntry?.savedStateHandle?.set("profiles", profiles)
                                                navController.navigate("profiles")
                                            } else {
                                                errorMessage = "Failed to fetch profiles: ${response.code()}"
                                            }
                                        }
                                        override fun onFailure(call: Call<ProfilesResponse>, t: Throwable) {
                                            errorMessage = "Network error: ${t.localizedMessage}"
                                        }
                                    })
                                } else {
                                    errorMessage = "Login failed: No token received."
                                }
                            }
                            400 -> errorMessage = "Login failed: Bad request. Please check your input."
                            401 -> errorMessage = "Login failed: Unauthorized. Check your credentials."
                            404 -> errorMessage = "Login failed: Endpoint not found. Contact support."
                            else -> errorMessage = "Login failed: ${response.code()} ${response.message()}"
                        }
                    }
                    override fun onFailure(call: Call<LoginResponse>, t: Throwable) {
                        isLoading = false
                        errorMessage = "Network error: ${t.localizedMessage}"
                    }
                })
            },
            modifier = Modifier.fillMaxWidth(),
            enabled = !isLoading
        ) {
            if (isLoading) CircularProgressIndicator(modifier = Modifier.size(24.dp))
            else Text("Login")
        }
        if (errorMessage.isNotEmpty()) {
            Spacer(modifier = Modifier.height(8.dp))
            Text(errorMessage, color = MaterialTheme.colorScheme.error)
        }
        Spacer(modifier = Modifier.height(8.dp))

        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            TextButton(onClick = { navController.navigate("signup") }) {
                Text("Sign Up")
            }
            TextButton(onClick = { navController.navigate("forgot_password") }) {
                Text("Forgot Password?")
            }
        }
    }
}

@Composable
fun HomeScreen(navController: NavController) {
    Box(
        modifier = Modifier.fillMaxSize(),
        contentAlignment = Alignment.Center
    ) {
        Column(horizontalAlignment = Alignment.CenterHorizontally) {
            Text("Welcome to Home Screen!")
            Spacer(modifier = Modifier.height(16.dp))
            Button(onClick = {
                navController.navigate("profile_update")
            }) {
                Text("Update Profile")
            }
        }
    }
}

@Composable
fun ForgotPasswordScreen(navController: NavController) {
    var emailOrMobile by remember { mutableStateOf("") }
    var isLoading by remember { mutableStateOf(false) }
    val context = LocalContext.current

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(32.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        OutlinedTextField(
            value = emailOrMobile,
            onValueChange = { emailOrMobile = it },
            label = { Text("Email or Mobile") },
            modifier = Modifier.fillMaxWidth()
        )
        Spacer(modifier = Modifier.height(16.dp))
        Button(
            onClick = {
                // No REST API call, just show a toast for demo
                Toast.makeText(context, "Reset Password pressed", Toast.LENGTH_SHORT).show()
                navController.navigate("login")
            },
            modifier = Modifier.fillMaxWidth(),
            enabled = !isLoading
        ) {
            if (isLoading) CircularProgressIndicator(modifier = Modifier.size(24.dp))
            else Text("Reset Password")
        }
    }
}

@Composable
fun SignupScreen(navController: NavController) {
    var emailOrMobile by remember { mutableStateOf("") }
    var fullName by remember { mutableStateOf("") }
    var dob by remember { mutableStateOf("") }
    var location by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    var rePassword by remember { mutableStateOf("") }
    val context = LocalContext.current
    val calendar = Calendar.getInstance()
    val dobInteractionSource = remember { androidx.compose.foundation.interaction.MutableInteractionSource() }
    var isLoading by remember { mutableStateOf(false) }
    val scrollState = rememberScrollState()

    LaunchedEffect(dobInteractionSource) {
        dobInteractionSource.interactions.collectLatest { interaction: Interaction ->
            if (interaction is FocusInteraction.Focus) {
                val datePicker = DatePickerDialog(
                    context,
                    { _, year, month, dayOfMonth ->
                        val formatted = "%02d-%02d-%04d".format(dayOfMonth, month + 1, year)
                        dob = formatted
                    },
                    calendar.get(Calendar.YEAR),
                    calendar.get(Calendar.MONTH),
                    calendar.get(Calendar.DAY_OF_MONTH)
                )
                datePicker.show()
            }
        }
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(scrollState)
            .padding(horizontal = 16.dp, vertical = 8.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Top
    ) {
        Image(
            painter = painterResource(id = R.drawable.company_logo),
            contentDescription = "Company Logo",
            modifier = Modifier.size(56.dp)
        )
        Spacer(modifier = Modifier.height(8.dp))
        Text(
            "Sign Up",
            style = MaterialTheme.typography.headlineMedium,
            color = MaterialTheme.colorScheme.primary
        )
        Spacer(modifier = Modifier.height(12.dp))

        OutlinedTextField(
            value = emailOrMobile,
            onValueChange = { emailOrMobile = it },
            label = { Text("Email or Mobile") },
            modifier = Modifier.fillMaxWidth()
        )
        Spacer(modifier = Modifier.height(8.dp))

        OutlinedTextField(
            value = fullName,
            onValueChange = { fullName = it },
            label = { Text("Full Name") },
            modifier = Modifier.fillMaxWidth()
        )
        Spacer(modifier = Modifier.height(8.dp))

        OutlinedTextField(
            value = dob,
            onValueChange = { dob = it },
            label = { Text("Date of Birth") },
            modifier = Modifier.fillMaxWidth(),
            interactionSource = dobInteractionSource
        )
        Spacer(modifier = Modifier.height(8.dp))

        OutlinedTextField(
            value = location,
            onValueChange = { location = it },
            label = { Text("Location") },
            modifier = Modifier.fillMaxWidth()
        )
        Spacer(modifier = Modifier.height(8.dp))

        OutlinedTextField(
            value = password,
            onValueChange = { password = it },
            label = { Text("Password") },
            visualTransformation = PasswordVisualTransformation(),
            modifier = Modifier.fillMaxWidth()
        )
        Spacer(modifier = Modifier.height(8.dp))

        OutlinedTextField(
            value = rePassword,
            onValueChange = { rePassword = it },
            label = { Text("Re-enter Password") },
            visualTransformation = PasswordVisualTransformation(),
            modifier = Modifier.fillMaxWidth()
        )
        Spacer(modifier = Modifier.height(12.dp))

        if (isLoading) {
            CircularProgressIndicator(modifier = Modifier.padding(8.dp))
        }

        Button(
            onClick = {
                // No REST API call, just show a toast for demo
                Toast.makeText(context, "Sign Up pressed", Toast.LENGTH_SHORT).show()
                navController.navigate("home")
            },
            modifier = Modifier.fillMaxWidth(),
            enabled = !isLoading
        ) {
            if (isLoading) CircularProgressIndicator(modifier = Modifier.size(24.dp))
            else Text("Sign Up")
        }
    }
}

@Composable
fun ProfileUpdateScreen(navController: NavController, user: User) {
    var fullName by remember { mutableStateOf(user.fullName) }
    var dob by remember { mutableStateOf(user.dob) }
    var location by remember { mutableStateOf(user.location) }
    var isLoading by remember { mutableStateOf(false) }
    val context = LocalContext.current
    val scrollState = rememberScrollState()

    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(scrollState)
            .padding(horizontal = 16.dp, vertical = 8.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Top
    ) {
        Text("Update Profile", style = MaterialTheme.typography.headlineMedium)
        Spacer(modifier = Modifier.height(12.dp))
        OutlinedTextField(
            value = fullName,
            onValueChange = { fullName = it },
            label = { Text("Full Name") },
            modifier = Modifier.fillMaxWidth()
        )
        Spacer(modifier = Modifier.height(8.dp))
        OutlinedTextField(
            value = dob,
            onValueChange = { dob = it },
            label = { Text("Date of Birth") },
            modifier = Modifier.fillMaxWidth()
        )
        Spacer(modifier = Modifier.height(8.dp))
        OutlinedTextField(
            value = location,
            onValueChange = { location = it },
            label = { Text("Location") },
            modifier = Modifier.fillMaxWidth()
        )
        Spacer(modifier = Modifier.height(12.dp))
        Button(
            onClick = {
                // No REST API call, just show a toast for demo
                Toast.makeText(context, "Update Profile pressed", Toast.LENGTH_SHORT).show()
                navController.navigate("home")
            },
            modifier = Modifier.fillMaxWidth(),
            enabled = !isLoading
        ) {
            if (isLoading) CircularProgressIndicator(modifier = Modifier.size(24.dp))
            else Text("Update Profile")
        }
    }
}

@Composable
fun ProfilesScreen(navController: NavController) {
    val profiles = navController.previousBackStackEntry?.savedStateHandle?.get<List<KidProfile>>("profiles")
    val iconColors = listOf(
        MaterialTheme.colorScheme.primary,
        MaterialTheme.colorScheme.secondary,
        MaterialTheme.colorScheme.tertiary,
        MaterialTheme.colorScheme.error,
        MaterialTheme.colorScheme.surfaceVariant
    )
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        horizontalAlignment = Alignment.Start,
        verticalArrangement = Arrangement.Top
    ) {
        Text("Profiles", style = MaterialTheme.typography.headlineMedium)
        Spacer(modifier = Modifier.height(16.dp))
        if (profiles == null || profiles.isEmpty()) {
            Text("No profiles found.")
        } else {
            profiles.forEachIndexed { index, profile ->
                val firstName = profile.name.split(" ").firstOrNull() ?: profile.name
                val iconColor = iconColors[index % iconColors.size]
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    modifier = Modifier.padding(vertical = 8.dp)
                ) {
                    // Circular icon with first letter of first name, different color for each
                    Box(
                        modifier = Modifier
                            .size(48.dp)
                            .background(
                                color = iconColor,
                                shape = CircleShape
                            ),
                        contentAlignment = Alignment.Center
                    ) {
                        Text(
                            text = firstName.firstOrNull()?.uppercase() ?: "?",
                            style = MaterialTheme.typography.headlineMedium,
                            color = MaterialTheme.colorScheme.onPrimary
                        )
                    }
                    Spacer(modifier = Modifier.width(16.dp))
                    Text(firstName, style = MaterialTheme.typography.bodyLarge)
                }
            }
        }
    }
}
