package com.aischool.app;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;
import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;
import java.util.List;

public class ProfileAdapter extends RecyclerView.Adapter<ProfileAdapter.ProfileViewHolder> {
    private List<KidProfile> profiles;
    private OnProfileClickListener listener;

    public interface OnProfileClickListener {
        void onProfileClick(KidProfile profile);
    }

    public ProfileAdapter(List<KidProfile> profiles, OnProfileClickListener listener) {
        this.profiles = profiles;
        this.listener = listener;
    }

    @NonNull
    @Override
    public ProfileViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.item_kid_profile, parent, false);
        return new ProfileViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull ProfileViewHolder holder, int position) {
        KidProfile profile = profiles.get(position);
        holder.bind(profile, listener);
    }

    @Override
    public int getItemCount() {
        return profiles.size();
    }

    static class ProfileViewHolder extends RecyclerView.ViewHolder {
        private TextView tvName, tvAge, tvGrade, tvGoals;

        public ProfileViewHolder(@NonNull View itemView) {
            super(itemView);
            tvName = itemView.findViewById(R.id.tvProfileName);
            tvAge = itemView.findViewById(R.id.tvProfileAge);
            tvGrade = itemView.findViewById(R.id.tvProfileGrade);
            tvGoals = itemView.findViewById(R.id.tvProfileGoals);
        }

        public void bind(KidProfile profile, OnProfileClickListener listener) {
            tvName.setText("👶 " + profile.getName());
            tvAge.setText("Age: " + profile.getAge());
            tvGrade.setText("📚 " + profile.getGrade());
            tvGoals.setText("🎯 " + profile.getLearningGoals());

            itemView.setOnClickListener(v -> {
                if (listener != null) {
                    listener.onProfileClick(profile);
                }
            });
        }
    }
}
