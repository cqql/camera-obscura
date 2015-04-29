package de.cqql.camera_obscura.android;

import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.AsyncTask;
import android.util.Log;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

public class UploadTask extends AsyncTask<Void, Void, Boolean> {
    private static final String URL = "http://192.168.178.62:5000/upload";

    private final RecordingActivity activity;
    private final String type;
    private final byte[] data;

    public UploadTask(RecordingActivity activity, String type, byte[] data) {
        this.activity = activity;
        this.type = type;
        this.data = data;
    }

    @Override
    protected Boolean doInBackground(Void... params) {
        Bitmap bitmap = BitmapFactory.decodeByteArray(data, 0, data.length);
        int width = 1024;
        int height = (int)((float)bitmap.getHeight() / (float)bitmap.getWidth() * width);
        Bitmap scaled = Bitmap.createScaledBitmap(bitmap, width, height, false);
        ByteArrayOutputStream stream = new ByteArrayOutputStream();
        scaled.compress(Bitmap.CompressFormat.JPEG, 90, stream);

        byte[] bytes = stream.toByteArray();

        Log.d(getClass().getName(), "Sending " + bytes.length + " bytes of " + type + " to " + URL);

        try {
            java.net.URL url = new URL(URL);

            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestProperty("Content-Type", type);
            connection.setDoOutput(true);
            connection.setFixedLengthStreamingMode(bytes.length);
            connection.getOutputStream().write(stream.toByteArray());
            connection.disconnect();
        } catch (MalformedURLException e) {
            Log.d(getClass().getName(), "Invalid URL: " + URL);
            return false;
        } catch (IOException e) {
            Log.d(getClass().getName(), "Could not upload picture: " + e.getMessage());
            // Not a bug. Keep sending for easier development.
            return true;
        }

        return true;
    }

    @Override
    protected void onPostExecute(Boolean succeeded) {
        if (succeeded) {
            activity.uploadDone();
        }
    }
}
