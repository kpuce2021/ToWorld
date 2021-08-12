package kr.ac.kpu.firstproject.ui

import android.content.Intent
import android.graphics.Typeface
import android.os.Build
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.view.MotionEvent
import android.view.View
import android.view.Window
import android.widget.Button
import androidx.annotation.RequiresApi
import androidx.core.content.ContextCompat
import kotlinx.android.synthetic.main.activity_tournament_create_popup.*
import kr.ac.kpu.firstproject.R

class TournamentCreatePopupActivity : AppCompatActivity() {

    // 이전에 어떤 버튼이 눌러져 있었는지 알 수 있도록 선언한 배열과 변수
    private lateinit var round_list : Array<Button>
    private var beforePushButton = 0

    @RequiresApi(Build.VERSION_CODES.LOLLIPOP)
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        setContentView(R.layout.activity_tournament_create_popup)
        initializedEventListener()
    }

    // 바깥 레이어 클릭 시 안닫히히게
    override fun onTouchEvent(event: MotionEvent?): Boolean {
        if(event?.action == MotionEvent.ACTION_OUTSIDE) return false
        return true
    }

    @RequiresApi(Build.VERSION_CODES.LOLLIPOP)
    private fun initializedEventListener() {
        round_list = arrayOf(findViewById(R.id.tournament_create_8_bt), findViewById(R.id.tournament_create_16_bt), findViewById(R.id.tournament_create_32_bt), findViewById(R.id.tournament_create_64_bt))

        tournament_create_bt.setOnClickListener {
            onTouchEventForStartButton(it)
        }

        tournament_create_8_bt.setOnClickListener {
            onTouchEventForRoundButton(it)
        }

        tournament_create_16_bt.setOnClickListener {
            onTouchEventForRoundButton(it)
        }

        tournament_create_32_bt.setOnClickListener {
            onTouchEventForRoundButton(it)
        }

        tournament_create_64_bt.setOnClickListener {
            onTouchEventForRoundButton(it)
        }
    }

    @RequiresApi(Build.VERSION_CODES.LOLLIPOP)
    private fun onTouchEventForRoundButton(view : View) {
        round_list[beforePushButton].background = getDrawable(R.drawable.button_border_line)
        round_list[beforePushButton].setTextColor(ContextCompat.getColor(this , R.color.colorTextForNotPushRoundButton))
        round_list[beforePushButton].typeface = Typeface.DEFAULT

        when(view.id) {
            R.id.tournament_create_8_bt -> {
                beforePushButton = 0
            }
            R.id.tournament_create_16_bt -> {
                beforePushButton = 1
            }
            R.id.tournament_create_32_bt -> {
                beforePushButton = 2
            }
            R.id.tournament_create_64_bt -> {
                beforePushButton = 3
            }
        }

        round_list[beforePushButton].background = getDrawable(R.drawable.push_button_border_line)
        round_list[beforePushButton].setTextColor(ContextCompat.getColor(this ,R.color.colorWordInColorPrimary))
        round_list[beforePushButton].typeface = Typeface.DEFAULT_BOLD
    }

    private fun onTouchEventForStartButton(view : View) {
        val intent = Intent(this.applicationContext, TournamentCreateActivity::class.java)
        intent.putExtra("ROUND", (8 * Math.pow(2.0, beforePushButton.toDouble())).toInt())
        startActivity(intent)
    }

}