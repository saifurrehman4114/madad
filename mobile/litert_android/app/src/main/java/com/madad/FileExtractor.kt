package com.madad

import android.content.Context
import java.io.File

/**
 * Copies a bundled asset to internal storage the first time it's requested
 * (LiteRT needs a real filesystem path, not an AssetManager stream). Uses
 * mmap'd reading so we don't load the entire 1.9 GB model into RAM.
 */
object FileExtractor {
    fun ensureAsset(ctx: Context, name: String): String {
        val target = File(ctx.filesDir, name)
        if (target.exists() && target.length() > 0) return target.absolutePath
        ctx.assets.open(name).use { input ->
            target.outputStream().use { out -> input.copyTo(out, bufferSize = 1 shl 20) }
        }
        return target.absolutePath
    }
}
