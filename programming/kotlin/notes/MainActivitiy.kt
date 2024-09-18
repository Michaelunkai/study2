package com.example.myapplication

import android.content.Context
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.example.myapplication.ui.theme.MyApplicationTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            MyApplicationTheme {
                Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
                    NoteTakingApp(this)
                }
            }
        }
    }
}

@Composable
fun NoteTakingApp(context: Context) {
    // Load existing notes from SharedPreferences
    val notes = remember {
        mutableStateOf(loadNotesFromSharedPreferences(context))
    }
    var newNoteText by remember { mutableStateOf("") }
    Column(modifier = Modifier.padding(16.dp)) {
        // Input field to add new notes
        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            OutlinedTextField(
                value = newNoteText,
                onValueChange = { newNoteText = it },
                label = { Text("Enter your note") },
                modifier = Modifier.weight(1f)
            )
            Button(
                onClick = {
                    if (newNoteText.isNotBlank()) {
                        notes.value.add(newNoteText)
                        // Save the updated notes to SharedPreferences
                        saveNotesToSharedPreferences(context, notes.value)
                        newNoteText = ""
                    }
                },
                modifier = Modifier.padding(start = 8.dp)
            ) {
                Text("Add")
            }
        }
        Spacer(modifier = Modifier.height(16.dp))
        // Display existing notes
        notes.value.forEach { note ->
            Text(text = note, modifier = Modifier.padding(8.dp))
        }
    }
}

private fun loadNotesFromSharedPreferences(context: Context): MutableList<String> {
    val sharedPreferences = context.getSharedPreferences("MyNotes", Context.MODE_PRIVATE)
    val notesSet = sharedPreferences.getStringSet("notes", setOf()) ?: setOf()
    return notesSet.toMutableList()
}

private fun saveNotesToSharedPreferences(context: Context, notes: List<String>) {
    val sharedPreferences = context.getSharedPreferences("MyNotes", Context.MODE_PRIVATE)
    sharedPreferences.edit().putStringSet("notes", notes.toSet()).apply()
}
