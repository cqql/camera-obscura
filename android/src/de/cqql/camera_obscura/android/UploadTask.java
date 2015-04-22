package de.cqql.camera_obscura.android;

import android.os.AsyncTask;
import android.util.Log;

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
        Log.d(getClass().getName(), "Sending " + data.length + " bytes of " + type + " to " + URL);

        try {
            java.net.URL url = new URL(URL);

            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestProperty("Content-Type", type);
            connection.setDoOutput(true);
            connection.setFixedLengthStreamingMode(data.length);
            connection.getOutputStream().write(data);
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
            activity.takePicture();
        }
    }
}
