package kr.ac.kpu.firstproject.ui

import android.annotation.SuppressLint
import android.content.Context
import android.os.Build
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.widget.LinearLayout
import androidx.annotation.RequiresApi
import androidx.core.content.ContextCompat
import kotlinx.android.synthetic.main.activity_tournament_create.*
import kr.ac.kpu.firstproject.R

class TournamentCreateActivity : AppCompatActivity() {

    private var round : Int = 8
    private val imageContainerList : ArrayList<View> = ArrayList()

    @RequiresApi(Build.VERSION_CODES.LOLLIPOP)
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_tournament_create)
        round = intent.getIntExtra("Round", 8)
        createViewForInsertImage()
        initializedEventListener()

    }

    @SuppressLint("WrongViewCast")
    private fun createViewForInsertImage(){
        val mInflater: LayoutInflater = getSystemService(Context.LAYOUT_INFLATER_SERVICE) as LayoutInflater
        val parent = findViewById<LinearLayout>(R.id.tournament_create_image_layout_container)

        var cnt = round / 2
        for(i in 0..cnt) {
            val view = mInflater.inflate(R.layout.tournament_image_container, parent, true)
            imageContainerList.add(view)
        }
    }

    @RequiresApi(Build.VERSION_CODES.LOLLIPOP)
    private fun initializedEventListener() {
        tournament_create_private_bt.setOnClickListener{
            onTouchEventForPublicButton(it)
        }

        tournament_create_public_bt.setOnClickListener{
            onTouchEventForPublicButton(it)
        }
    }

    @RequiresApi(Build.VERSION_CODES.LOLLIPOP)
    private fun onTouchEventForPublicButton(view: View){
        when(view.id){
            R.id.tournament_create_public_bt -> {
                tournament_create_passwd_et.visibility = View.INVISIBLE
                tournament_create_private_bt.background = getDrawable(R.drawable.button_border_line)
                tournament_create_private_bt.setTextColor(ContextCompat.getColor(this , R.color.colorTextForNotPushButton))

                tournament_create_public_bt.background = getDrawable(R.drawable.push_button_border_line)
                tournament_create_public_bt.setTextColor(ContextCompat.getColor(this , R.color.colorWordInColorPrimary))
            }

            R.id.tournament_create_private_bt -> {
                tournament_create_public_bt.background = getDrawable(R.drawable.button_border_line)
                tournament_create_public_bt.setTextColor(ContextCompat.getColor(this , R.color.colorTextForNotPushButton))

                tournament_create_passwd_et.visibility = View.VISIBLE
                tournament_create_private_bt.background = getDrawable(R.drawable.push_button_border_line)
                tournament_create_private_bt.setTextColor(ContextCompat.getColor(this , R.color.colorWordInColorPrimary))
            }
        }
    }
}