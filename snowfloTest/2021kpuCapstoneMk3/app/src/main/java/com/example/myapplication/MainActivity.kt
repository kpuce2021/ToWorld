package com.example.myapplication

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.text.TextUtils
import android.view.animation.AnimationUtils
import android.widget.Toast
import com.google.firebase.auth.FirebaseAuth
import kotlinx.android.synthetic.main.activity_main.*
import kotlinx.android.synthetic.main.activity_main.make_account_text

// 메인
class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        
        // 로딩창
        val alertMessageAnim = AnimationUtils.loadAnimation(applicationContext, R.anim.alert_message_animation)
        
        // 로그인 버튼 이벤트
        login_button.setOnClickListener {
            
            when {  // 공백 체크
                TextUtils.isEmpty(input_email.text.toString().trim() { it <= ' ' }) -> {
                    Toast.makeText(this@MainActivity,"이메일을 입력하시오", Toast.LENGTH_SHORT).show()
                }
                TextUtils.isEmpty(input_pswd.text.toString().trim() { it <= ' ' }) -> {
                    Toast.makeText(this@MainActivity,"비밀번호를 입력하시오", Toast.LENGTH_SHORT).show()
                }
                else -> {  // 로그인 체크
                    val email = input_email.text.toString().trim() { it <= ' ' }
                    val password = input_pswd.text.toString().trim() { it <= ' ' }

                    FirebaseAuth.getInstance().signInWithEmailAndPassword(email, password)
                        .addOnCompleteListener { task ->
                            if (task.isSuccessful) {  // 인증 성공

                                val loginIntent = Intent(this, ServiceActivity::class.java)

                                loginIntent.flags =
                                    Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK //새로운 Activity를 수행하고 현재 Activity를 스택에서 제거하기
                                loginIntent.putExtra("user_id",FirebaseAuth.getInstance().currentUser!!.uid)
                                loginIntent.putExtra("user_email",input_email.text.toString())
                                startActivity(loginIntent)
                                finish()

                            } else {  // 인증 실패
                                alert_message.startAnimation(alertMessageAnim)
                            }
                        }


                    }
                }
            }
        make_account_text.setOnClickListener {  // 회원 가입
            val intent = Intent(this, makeAccountActivity::class.java)
            startActivity(intent)
        }
    }
}