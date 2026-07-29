package com.zalexdev.stryker.appintro.slides;


import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

import com.google.android.material.button.MaterialButton;
import com.zalexdev.stryker.MainActivity;
import com.zalexdev.stryker.R;

public class Slide6Final extends Fragment {

    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.new_slide5, container, false);
        MaterialButton button = view.findViewById(R.id.login);
        button.setOnClickListener(view1 -> {
            Activity activity = getActivity();
            if (activity != null && !activity.isFinishing()) {
                Intent main = new Intent(activity, MainActivity.class);
                main.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
                activity.startActivity(main);
                activity.finish();
            }
        });
        return view;
    }
}
