package com.madad

import org.json.JSONArray
import org.json.JSONObject

/** Tolerant JSON decode for Gemma output — strips fences, finds the brace block. */
object JsonParser {
    data class SignResult(
        val glosses: List<String>,
        val urdu: String,
        val english: String,
        val confidence: Float,
        val notes: String?,
    )

    fun parseSignResult(raw: String): SignResult? {
        val cleaned = strip(raw)
        return runCatching {
            val j = JSONObject(cleaned)
            SignResult(
                glosses = j.optJSONArray("glosses").toStringList(),
                urdu = j.optString("urdu", ""),
                english = j.optString("english", ""),
                confidence = j.optDouble("confidence", 0.0).toFloat(),
                notes = j.optString("notes").takeIf { it.isNotBlank() },
            )
        }.getOrNull()
    }

    private fun strip(s: String): String {
        var t = s.trim().removePrefix("```json").removePrefix("```").removeSuffix("```").trim()
        val start = t.indexOf('{')
        val end = t.lastIndexOf('}')
        if (start in 0..end) t = t.substring(start, end + 1)
        return t
    }

    private fun JSONArray?.toStringList(): List<String> {
        if (this == null) return emptyList()
        val out = mutableListOf<String>()
        for (i in 0 until length()) out.add(optString(i))
        return out
    }
}
