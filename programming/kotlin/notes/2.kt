package com.example.notes

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
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Delete
import com.example.notes.ui.theme.NotesTheme // Updated import

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            NotesTheme { // Updated theme usage
                NoteTakingApp(this)
            }
        }
    }
}

@Composable
fun NoteTakingApp(context: Context) {
    val notes = remember {
        mutableStateOf(loadNotesFromSharedPreferences(context))
    }
    var newNoteText by remember { mutableStateOf("") }
    Column(modifier = Modifier.padding(16.dp)) {
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
        notes.value.forEachIndexed { index, note ->
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(bottom = 8.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(text = note, modifier = Modifier.weight(1f))
                IconButton(
                    onClick = {
                        notes.value.removeAt(index)
                        saveNotesToSharedPreferences(context, notes.value)
                    }
                ) {
                    Icon(
                        imageVector = Icons.Filled.Delete,
                        contentDescription = "Delete note"
                    )
                }
            }
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
