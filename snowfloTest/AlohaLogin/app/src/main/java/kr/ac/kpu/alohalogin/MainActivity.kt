package kr.ac.kpu.alohalogin

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.view.animation.AnimationUtils
import kotlinx.android.synthetic.main.activity_main.*

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)


        val alertMessageAnim = AnimationUtils.loadAnimation(applicationContext, R.anim.alert_message_animation)


        login_button.setOnClickListener {
            alert_message.startAnimation(alertMessageAnim)
        }

        make_account_text.setOnClickListener {
            val intent = Intent(this , makeAccountActivity::class.java)
            startActivity(intent)
        }
    }

}